from django.db import models
from django.core.mail import EmailMultiAlternatives
from taggit.managers import TaggableManager
from care.sms.twilio import twilio_client
import shortuuid
from django.db import transaction
from django.conf import settings
import pytz
from django.core import mail


def get_uuid(length=10):
    uid = shortuuid.ShortUUID()
    uid.set_alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return uid.random(length=length)


class Facility(models.Model):
    identity = models.CharField(max_length=100, editable=False, unique=True)
    name = models.CharField(max_length=255)
    facility_size = models.CharField(max_length=20, blank=True, null=True)
    cluster = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    liaisons = models.CharField(max_length=255, blank=True, null=True)
    emails = models.TextField(blank=True, null=True)
    phones = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True) # used for facility type/etc.
    reporting_new_cases = models.BooleanField(default=False)
    last_new_cases_reported = models.IntegerField(default=0)
    last_upload_date = models.DateTimeField(blank=True, null=True)
    last_message_date = models.DateTimeField(blank=True, null=True)
    last_sms_date = models.DateTimeField(blank=True, null=True)
    last_message_open_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    # hopefully this is safe...
    def save(self, *args, **kwargs):
        # new instance, insert a UUID if one is not provided in kwargs
        if not self.pk:
            if 'identity' not in kwargs:
                self.identity = get_uuid()
        super(Facility, self).save(*args, **kwargs)

    def qualtrics_link(self):
        all_tags = self.tags.names()
        is_behavioral = list(set(all_tags) & set(settings.BEHAVIORAL_TAGS))
        if len(is_behavioral) > 0:
            return settings.QUALTRICS_SURVEY_LINK_BEHAVIORAL
        else:
            return settings.QUALTRICS_SURVEY_LINK

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# Twilio Binding for Facilities - to be used for SMS/Voice
class Binding(models.Model):
    class BindingType(models.TextChoices):
        SMS = 'sms'
        FB = 'facebook-messenger'
        APN = 'apn'
        FCM = 'fcm'
        GCM = 'gcm'

    service_sid = models.CharField(max_length=255) # Twilio Service the Binding is tied to
    binding_sid = models.CharField(max_length=255) # unique ID for this binding
    binding_type = models.CharField(
        max_length=20,
        choices=BindingType.choices,
        default=BindingType.SMS
    )
    opt_out = models.BooleanField(default=False)
    address = models.CharField(max_length=255, help_text='Phone number, e.g. +15205551234') # initially going to be phone number for SMS addresses
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # create the actual twilio binding reflected by this object.
        # deletion of the twilio binding occurs in signals.py
        if not self.pk:
            binding = twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings.create(identity=self.facility.identity, binding_type=self.binding_type, address=self.address)
            self.binding_sid = binding.sid
            self.service_sid = binding.service_sid
        super(Binding, self).save(*args, **kwargs)

    def __unicode__(self):
        return f'{self.facility.name} - {self.address}'

    def __str__(self):
        return f'{self.facility.name} - {self.address}'

    class Meta:
        verbose_name = "SMS Number"
        verbose_name_plural = "SMS Numbers"


class QualtricsSubmission(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, blank=True, null=True)
    facility_name = models.CharField(max_length=200, blank=True, null=True)
    reported_new_cases = models.BooleanField(default=False)
    new_cases = models.IntegerField(default=0)

    def __unicode__(self):
        return f'{self.facility_name} {self.created_date:%Y-%m-%d %H:%M}'

    def __str__(self):
        return f'{self.facility_name} {self.created_date:%Y-%m-%d %H:%M}'


class TwilioConversation(models.Model):
    sid = models.CharField(max_length=200)
    account_sid = models.CharField(max_length=200)
    chat_service_sid = models.CharField(max_length=200)
    messaging_service_sid = models.CharField(max_length=200)
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.sid

    def __str__(self):
        return self.sid


class TwilioMessage(models.Model):
    body = models.TextField()
    index = models.PositiveIntegerField()
    conversation = models.ForeignKey(TwilioConversation, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, blank=True, null=True)
    author_sid = models.CharField(max_length=200, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return f'{self.conversation} - {self.index}'

    def __str__(self):
        return f'{self.conversation} - {self.index}'


def send_sms_message(uuid, message, bulk=False):
    if bulk:
        sms_users = list(Facility.objects.filter(identity__in=uuid).values_list('identity', flat=True))
        if len(sms_users) > 0:
            # separate the users into 20-long buckets since that's the max twilio can do.
            for chunk in [sms_users[x:x+20] for x in range(0, len(sms_users), 20)]:
                twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).notifications.create(
                    identity=chunk,
                    body=message,
                )
    else:
        # twilio requires the identities to be in a list, even if it's just one.
        if type(uuid) is not list:
            uuid = [uuid]
        twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).notifications.create(
            identity=uuid,
            body=message,
        )


def send_email_message(uuid, subject, message, attachment_filename=None, attachment_content=None, attachment_mimetype=None, bulk=False):
    email_message = None
    if bulk:
        email_facilities = list(Facility.objects.filter(identity__in=uuid).values_list('emails', flat=True))
        if len(email_facilities) > 0:
            emails = []
            for facility in email_facilities:
                for email in facility.split(';'):
                    emails.append(email.strip())
            # subject, message, from, to, to_cc, to_bcc,
            email_message = EmailMultiAlternatives(subject, message, settings.SENDGRID_FROM_EMAIL, [emails[0]], emails[1:], reply_to=[settings.SENDGRID_REPLY_TO_EMAIL])
    else:
        facility = Facility.objects.get(identity=uuid)
        emails = []
        for email in facility.emails.split(';'):
            emails.append(email.strip())
        if len(emails) > 1:
            email_message = EmailMultiAlternatives(subject, message, settings.SENDGRID_FROM_EMAIL, [emails[0]], emails[1:], reply_to=[settings.SENDGRID_REPLY_TO_EMAIL])
        else:
            email_message = EmailMultiAlternatives(subject, message, settings.SENDGRID_FROM_EMAIL, [emails[0]], reply_to=[settings.SENDGRID_REPLY_TO_EMAIL])
    if email_message:
        if attachment_filename is not None and attachment_content is not None and attachment_mimetype is not None:
            email_message.attach(attachment_filename, attachment_content, attachment_mimetype)
        with mail.get_connection() as connection:
            connection.send_messages([email_message])
