from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from care.sms.utils import CLUSTER_WEEKLY_TPL
from django.utils import timezone
import pytz


AMERICA_PHOENIX = pytz.timezone('America/Phoenix')


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to Facilities that have cluster status weekly if they have not submitted in a week.'

    def handle(self, *args, **options):
        now = timezone.now().astimezone(AMERICA_PHOENIX)
        # if the SMS_ENABLED setting isn't defined yet, assume we want it enabled.
        sms_enabled = getattr(settings, 'SMS_ENABLED', True)
        if sms_enabled:
            for facility in Facility.objects.filter(cluster=True):
                do_message = False
                if facility.last_upload_date is not None:
                    delta_since_last_upload = now - facility.last_upload_date
                    if facility.last_sms_date is not None:
                        delta_since_last_sms = now - facility.last_sms_date
                        # if both are 3 or more days, send another text.
                        # (e.g. should only ever get a text every 3 days, if they haven't submitted in 3 days)
                        if delta_since_last_upload.days >= 3 and delta_since_last_sms.days >= 3:
                            do_message = True
                    else:
                    # facility has not been texted before
                    # just check if the upload date is 3 or more days in the past
                        if delta_since_last_upload.days >= 3:
                            # send them a message.
                            do_message = True
                else:
                    # always send a message if the last upload date is null,
                    # as long as they haven't been messaged in the past 3 days.
                    if facility.last_sms_date is not None:
                        delta_since_last_sms = now - facility.last_sms_date
                        if delta_since_last_sms.days >= 3:
                            do_message = True
                    else:
                        # and if the last sms date is also null, send them a reminder.
                        do_message = True
                if do_message:
                    sms_message = CLUSTER_WEEKLY_TPL['sms'].format(uuid=facility.identity, link=facility.qualtrics_link())
                    send_sms_message(facility.identity, sms_message, bulk=False)
                    facility.last_sms_date = now
                    facility.save()
