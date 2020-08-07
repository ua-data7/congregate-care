from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import CLUSTER_DAILY_TPL
from django.utils import timezone
import pytz
import os


AMERICA_PHOENIX = pytz.timezone('America/Phoenix')

attachment_filename = 'Linelist_Instruction.pdf'
attachment_path = os.path.join(settings.BASE_DIR, 'sms', 'templates', 'messages', attachment_filename)
with open(attachment_path, 'rb+') as f:
    attachment_content = f.read()
attachment_mimetype = 'application/pdf'


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to Facilities that have cluster status daily.'
    # to be scheduled in a cron job at 3pm weekdays (no sat/sun).
    def handle(self, *args, **options):
        az_now = timezone.now().astimezone(AMERICA_PHOENIX)
        email_enabled = getattr(settings, 'EMAIL_ENABLED', True)
        sms_enabled = getattr(settings, 'SMS_ENABLED', True)
        for facility in Facility.objects.filter(cluster=True):
            link = facility.qualtrics_link()
            sms_message = CLUSTER_DAILY_TPL['sms'].format(uuid=facility.identity, link=link)
            email_message = CLUSTER_DAILY_TPL['email'].format(uuid=facility.identity, link=link, facility_name=facility.name)
            if sms_enabled:
                send_sms_message(facility.identity, sms_message, bulk=False)
            if email_enabled:
                send_email_message(facility.identity, CLUSTER_DAILY_TPL['subject'], email_message, bulk=False, attachment_filename=attachment_filename, attachment_content=attachment_content, attachment_mimetype=attachment_mimetype)
                facility.last_message_date = az_now
            facility.save()
