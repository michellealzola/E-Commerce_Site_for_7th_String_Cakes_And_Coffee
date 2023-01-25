import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seventh_string_3.settings')
app = Celery('seventh_string_3')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
