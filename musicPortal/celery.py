import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicPortal.settings' )


app = Celery('musicPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()