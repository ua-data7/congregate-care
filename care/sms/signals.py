from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
from care.sms.twilio import twilio_client
from care.sms.models import Binding
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from sentry_sdk import capture_exception


@receiver(pre_delete, sender=Binding)
def remove_binding(sender, instance, **kwargs):
    try:
        twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings(instance.binding_sid).delete()
    except TwilioRestException as e:
        capture_exception(e)


@receiver(pre_save, sender=Binding)
def opt_out_binding(sender, instance, **kwargs):
    try:
        real_obj = Binding.objects.get(id=instance.pk)
    except Binding.DoesNotExist:
        # new binding or non-existing binding, so change detection doesn't make sense.
        return
    if not real_obj.opt_out and instance.opt_out:
        # this binding is opting out. delete the binding from twilio
        twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings(instance.binding_sid).delete()
    elif real_obj.opt_out and not instance.opt_out:
        # this binding is opting back in. re-create it and update the object with new binding sid
        binding = twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings.create(identity=instance.facility.identity, binding_type=instance.binding_type, address=instance.address)
        instance.binding_sid = binding.sid
