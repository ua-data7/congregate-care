from django.apps import AppConfig


class SmsConfig(AppConfig):
    name = 'care.sms'

    def ready(self):
        import care.sms.signals
