from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import NON_CLUSTER_WEEKLY_TPL, CLUSTER_WEEKLY_TPL, LIAISON_WEEKLY_TPL
import os
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.core import mail


attachment_filename = 'LTC Facility Linelist Template Final.xls'
attachment_path = os.path.join(settings.BASE_DIR, 'sms', 'templates', 'messages', attachment_filename)
with open(attachment_path, 'rb+') as f:
    attachment_content = f.read()
attachment_mimetype = 'application/vnd.ms-excel'


class Command(BaseCommand):
    help = 'Sends a reminder to non-cluster Facilities weekly.'
    # to be scheduled in a cron job at 9am Mondays.
    def handle(self, *args, **options):
        now = timezone.now()
        non_cluser_facilities = {}
        cluster_facilities = {}
        email_enabled = getattr(settings, 'EMAIL_ENABLED', True)
        sms_enabled = getattr(settings, 'SMS_ENABLED', True)
        for key in settings.LIAISON_EMAIL_MAP.keys():
            non_cluser_facilities[key] = []
            cluster_facilities[key] = []
        for facility in Facility.objects.filter(cluster=False):
            do_message = False
            if facility.last_upload_date is not None:
                delta_since_last_upload = now - facility.last_upload_date
                if delta_since_last_upload.days > 6:
                    # send them a message.
                    do_message = True
            else:
                do_message = True
            if do_message:
                if email_enabled:
                    email_message = NON_CLUSTER_WEEKLY_TPL['email'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK, facility_name=facility.name)
                    send_email_message(facility.identity, NON_CLUSTER_WEEKLY_TPL['subject'], email_message, bulk=False, attachment_filename=attachment_filename, attachment_content=attachment_content, attachment_mimetype=attachment_mimetype)
                if sms_enabled:
                    sms_message = NON_CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                    send_sms_message(facility.identity, sms_message, bulk=False)
                if facility.liaisons in non_cluser_facilities:
                    non_cluser_facilities[facility.liaisons].append(f'{facility.name} - {facility.identity}')
                facility.last_message_date = now
                facility.save()
        for facility in Facility.objects.filter(cluster=True):
            do_message = False
            if facility.last_upload_date is not None:
                delta_since_last_upload = now - facility.last_upload_date
                if delta_since_last_upload.days > 6:
                    # send them a message.
                    do_message = True
            else:
                do_message = True
            if do_message:
                if email_enabled:
                    email_message = CLUSTER_WEEKLY_TPL['email'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK, facility_name=facility.name)
                    send_email_message(facility.identity, CLUSTER_WEEKLY_TPL['subject'], email_message, bulk=False, attachment_filename=attachment_filename, attachment_content=attachment_content, attachment_mimetype=attachment_mimetype)
                if sms_enabled:
                    sms_message = CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                    send_sms_message(facility.identity, sms_message, bulk=False)
                if facility.liaisons in cluster_facilities:
                    cluster_facilities[facility.liaisons].append(f'{facility.name} - {facility.identity}')
                facility.last_message_date = now
                facility.save()
        for key in settings.LIAISON_EMAIL_MAP.keys():
            if (len(non_cluser_facilities[key]) > 0) or (len(cluster_facilities[key]) > 0):
                to_emails = settings.LIAISON_EMAIL_MAP[key]
                if len(non_cluser_facilities[key]) > 0:
                    non_cluser_facilities_txt = '\n'.join(non_cluser_facilities[key])
                else:
                    non_cluser_facilities_txt = 'None\n'
                if len(cluster_facilities[key]) > 0:
                    cluster_facilities_txt = '\n'.join(cluster_facilities[key])
                else:
                    cluster_facilities_txt = 'None\n'
                message = LIAISON_WEEKLY_TPL['message'].format(non_cluser_facilities=non_cluser_facilities_txt, cluster_facilities=cluster_facilities_txt)
                email_message = EmailMultiAlternatives(LIAISON_WEEKLY_TPL['subject'], message, settings.SENDGRID_FROM_EMAIL, [to_emails[0]], to_emails[1:], settings.LIAISON_EMAIL_MAP[key][0], reply_to=[settings.SENDGRID_REPLY_TO_EMAIL])
                with mail.get_connection() as connection:
                    connection.send_messages([email_message])
