from django.db import models
from django.core.mail import EmailMessage
from taggit.managers import TaggableManager
from care.sms.twilio import twilio_client
import shortuuid
from django.db import transaction
from django.conf import settings
import pytz


class PreferredContactType(models.TextChoices):
    EMAIL = 'email'
    SMS = 'sms'
    VOICE = 'voice'


class Facility(models.Model):
    identity = models.CharField(max_length=100, editable=False, unique=True)
    name = models.CharField(max_length=255)
    facility_size = models.CharField(max_length=20, blank=True, null=True)
    cluster = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    liasons = models.CharField(max_length=255, blank=True, null=True)
    emails = models.TextField(blank=True, null=True)
    phones = models.TextField(blank=True, null=True)
    preferred_contact = models.CharField(
        max_length=10,
        choices=PreferredContactType.choices,
        default=PreferredContactType.SMS
    )
    tags = TaggableManager(blank=True) # used for facility type/etc.
    reporting_new_cases = models.BooleanField(default=False)
    last_new_cases_reported = models.IntegerField(default=0)
    last_upload_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

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
    address = models.CharField(max_length=255) # initially going to be phone number for SMS addresses
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'{self.facility.name} - {self.address}'

    def __str__(self):
        return f'{self.facility.name} - {self.address}'


def get_uuid(length=10):
    uid = shortuuid.ShortUUID()
    uid.set_alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return uid.random(length=length)


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

# Facility will have to exist prior to the binding for its SMS numbers being created.
def create_binding(uuid, address, binding_type='sms'):
    if not address:
        raise ValueError('address is a required parameter.')
    if not uuid:
        raise ValueError('uuid is a required parameter.')
    if not Binding.objects.filter(address=address).exists():
        with transaction.atomic():
            binding = twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings.create(identity=uuid, binding_type=binding_type, address=address)
            facility = Facility.objects.get(identity=uuid)
            Binding.objects.create(
                service_sid=settings.TWILIO_NOTIFICATION_SERVICE_SID,
                address=address,
                binding_type=binding_type,
                facility=facility,
                binding_sid=binding.sid,
            )
            return uuid
    else:
        # a Binding with the given address already exists.
        raise IntegrityError('A binding for this address already exists.')


def send_sms_message(uuid, message, bulk=False):
    if bulk:
        sms_users = list(Facility.objects.filter(identity__in=uuid).values_list('identity', flat=True))
        # use messaging/notify service.
        if len(sms_users) > 0:
            twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).notifications.create(
                identity=sms_users,
                body=message,
            )
    else:
        twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).notifications.create(
            identity=uuid,
            body=message,
        )


def send_email_message(uuid, subject, message, bulk=False):
    if bulk:
        email_facilities = list(Facility.objects.filter(identity__in=uuid).values_list('emails', flat=True))
        if len(email_users) > 0:
            emails = []
            for facility in email_facilities:
                for email in facility.split(','):
                    emails.append(email)
            # subject, message, from, to, to_cc, to_bcc, 
            email_message = EmailMessage(subject, message, settings.SENDGRID_FROM_EMAIL, emails[0], None, emails[1:])
            email_message.send()
    else:
        facility = Facility.objects.get(identity=uuid)
        emails = facility.emails.split(',')
        if len(emails) > 1:
            email_message = EmailMessage(subject, message, settings.SENDGRID_FROM_EMAIL, emails[0], None, emails[1:])
        else:
            email_message = EmailMessage(subject, message, settings.SENDGRID_FROM_EMAIL, emails[0])
        email_message.send()
