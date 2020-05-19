from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import CLUSTER_WEEKLY_TPL
import pytz
import os


attachment_filename = 'LTC Facility Linelist Template Final.xls'
attachment_path = os.path.join(settings.BASE_DIR, 'sms', 'templates', 'messages', attachment_filename)
with open(attachment_path, 'rb+') as f:
    attachment_content = f.read()
attachment_mimetype = 'application/vnd.ms-excel'


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to Facilities that have cluster status weekly if they have not submitted in a week.'

    def handle(self, *args, **options):
        az_now = pytz.timezone('America/Phoenix').localize(pytz.datetime.datetime.now())
        for facility in Facility.objects.filter(cluster=True):
            do_message = False
            if facility.last_upload_date is not None:
                delta_since_last_upload = az_now - facility.last_upload_date
                if delta_since_last_upload.days > 6:
                    # send them a message.
                    do_message = True
            else:
                do_message = True
            if do_message:
                email_message = CLUSTER_WEEKLY_TPL['email'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                sms_message = CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                send_sms_message(facility.identity, sms_message, bulk=False)
                send_email_message(facility.identity, CLUSTER_WEEKLY_TPL['subject'], email_message, bulk=False, attachment_filename=attachment_filename, attachment_content=attachment_content, attachment_mimetype=attachment_mimetype)
                facility.last_message_date = az_now
                facility.save()
