from care.sms.models import send_sms_message, send_email_message
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Sends a reminder with link to survey to SMS/email users'

    def handle(self, *args, **options):
        for user in EnrolledUser.objects.filter(preferred_contact=PreferredContactType.SMS):
            message = f'Please update your facility status at {settings.QUALTRICS_SURVEY_LINK}?uuid={user.uuid}'
            send_sms_message(user.identity, message, bulk=False)
        for user in EnrolledUser.objects.filter(preferred_contact=PreferredContactType.EMAIL):
            message = f'Hello {user.name},\nPlease update your facility status at {settings.QUALTRICS_SURVEY_LINK}?uuid={user.uuid}\nRegards, Pima County Health Department'
            send_email_message(user.uuid, settings.DEFAULT_REMINDER_EMAIL_SUBJECT, message, bulk=False)
