from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import *
from . tasks import schedule_appointment_reminder
import datetime

@receiver(post_save, sender = Appointment)
def appointment_created(sender, instance, created, **kwargs):
    if created:
        print(f"[📶 Signal Triggered] Appointment created for {instance.user.email} at {instance.scheduled_time}")
        
        reminder_time = instance.scheduled_time - datetime.timedelta(hours=1)
        schedule_appointment_reminder.apply_async(
            args = [instance.user.email,
                    instance.title,
                    str(instance.scheduled_time)],
            eta = reminder_time        # Estimated Time of Arrival
        )