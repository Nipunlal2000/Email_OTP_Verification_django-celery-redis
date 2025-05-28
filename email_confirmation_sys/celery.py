import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_confirmation_sys.settings')

app = Celery('email_confirmation_sys')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Optional: use DatabaseScheduler if using django-celery-beat
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


# app.conf.beat_schedule = {
#     'send_hourly_user_report': {
#         'task': 'email_app.tasks.send_hourly_user_report',
#         'schedule': crontab(minute='*/60'),  # every 1 hour (for testing)
#     },
# }


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')