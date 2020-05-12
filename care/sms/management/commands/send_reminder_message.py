from care.sms.models import send_sms_message, send_email_message
from care.sms.models import Facility
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to SMS/email users'

    def handle(self, *args, **options):
        for facility in Facility.objects.filter(preferred_contact=PreferredContactType.SMS):
            message = f'Please update your facility status at {settings.QUALTRICS_SURVEY_LINK}?uuid={facility.identity}'
            send_sms_message(facility.identity, message, bulk=False)
        for facility in Facility.objects.filter(preferred_contact=PreferredContactType.EMAIL):
            message = f'Hello {facility.name},\nPlease update your facility status at {settings.QUALTRICS_SURVEY_LINK}?uuid={facility.identity}\nRegards, Pima County Health Department'
            send_email_message(facility.identity, settings.DEFAULT_REMINDER_EMAIL_SUBJECT, message, bulk=False)
