from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
from care.sms.twilio import twilio_client
from care.sms.models import Binding
from django.conf import settings


@receiver(pre_delete, sender=Binding)
def remove_binding(sender, instance, **kwargs):
    twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings(instance.binding_sid).delete()

@receiver(pre_save, sender=Binding)
def opt_out_binding(sender, instance, **kwargs):
    real_obj = Binding.objects.get(id=instance.pk)
    if not real_obj.opt_out and instance.opt_out:
        # this binding is opting out. delete the binding from twilio
        twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings(instance.binding_sid).delete()
    elif real_obj.opt_out and not instance.opt_out:
        # this binding is opting back in. re-create it and update the object with new binding sid
        binding = twilio_client.notify.services(settings.TWILIO_NOTIFICATION_SERVICE_SID).bindings.create(identity=instance.facility.identity, binding_type=instance.binding_type, address=instance.address)
        instance.binding_sid = binding.sid