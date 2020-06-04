from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import CLUSTER_WEEKLY_TPL
import pytz
import os


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to Facilities that have cluster status weekly if they have not submitted in a week.'

    def handle(self, *args, **options):
        az_now = pytz.timezone('America/Phoenix').localize(pytz.datetime.datetime.now())
        for facility in Facility.objects.filter(cluster=True):
            do_message = False
            if facility.last_upload_date is not None:
                delta_since_last_upload = az_now - facility.last_upload_date
                if delta_since_last_upload.days >= 3:
                    # send them a message.
                    do_message = True
            else:
                do_message = True
            if do_message:
                sms_message = CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=settings.QUALTRICS_SURVEY_LINK)
                send_sms_message(facility.identity, sms_message, bulk=False)
                facility.last_message_date = az_now
                facility.save()
