from __future__ import absolute_import
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiffyCalendar.settings')
    
from django.conf import settings
from celery import Celery
    
app = Celery('spiffyCalendar',)
# backend='rpc://',
# broker='amqp://guest:guest@localhost//5672'
    
# This reads, e.g., CELERY_ACCEPT_CONTENT = ['json'] from settings.py:
app.config_from_object('django.conf:settings', namespace='CELERY')
    
# For autodiscover_tasks to work, you must define your tasks in a file called 'tasks.py'.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    
@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))