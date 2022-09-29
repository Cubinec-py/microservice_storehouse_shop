import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_for_books': {
        'task': 'books.tasks.check_for_books',
        'schedule': crontab(minute='*/2'),
    },
    'update_count_books': {
        'task': 'books.tasks.update_count_books',
        'schedule': crontab(minute='*/1'),
    },
}
