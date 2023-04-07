import os

from celery import Celery
from django.conf import settings

# from vpscrapproject import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpscrapproject.settings")
# app = Celery('vpscrapproject', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app = Celery("vpscrapproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# app.conf.broker_url = "amqp://admin:admin2023@rabbitmq//"
# print(app.conf.broker_url)
# Load task modules from all registered Django apps.


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
