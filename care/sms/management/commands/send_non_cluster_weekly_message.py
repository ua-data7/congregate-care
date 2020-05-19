from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import NON_CLUSTER_WEEKLY_TPL
import os
import pytz


attachment_filename = 'LTC Facility Linelist Template Final.xls'
attachment_path = os.path.join(settings.BASE_DIR, 'sms', 'templates', 'messages', attachment_filename)
with open(attachment_path, 'rb+') as f:
    attachment_content = f.read()
attachment_mimetype = 'application/vnd.ms-excel'


class Command(BaseCommand):
    help = 'Sends a reminder to non-cluster Facilities weekly.'

    def handle(self, *args, **options):
        az_now = pytz.timezone('America/Phoenix').localize(pytz.datetime.datetime.now())
        for facility in Facility.objects.filter(cluster=False):
            do_message = False
            if facility.last_upload_date is not None:
                delta_since_last_upload = az_now - facility.last_upload_date
                if delta_since_last_upload.days > 6:
                    # send them a message.
                    do_message = True
            else:
                do_message = True
            if do_message:
                email_message = NON_CLUSTER_WEEKLY_TPL['email'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                sms_message = NON_CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                send_email_message(facility.identity, NON_CLUSTER_WEEKLY_TPL['subject'], email_message, bulk=False, attachment_filename=attachment_filename, attachment_content=attachment_content, attachment_mimetype=attachment_mimetype)
                send_sms_message(facility.identity, sms_message, bulk=False)
                facility.last_message_date = az_now
                facility.save()
