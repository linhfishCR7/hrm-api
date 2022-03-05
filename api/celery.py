# Python imports
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(
    worker_pool_restarts=True,
)

# Celery Beat Config
# app.conf.beat_schedule = {
#     'set_ratings_matrix_to_cache': {
#         'task': 'base.tasks.set_ratings_matrix_to_cache',
#         'schedule': crontab(minute=0, hour="*/2")
#     }
# }

app.conf.beat_schedule = {

}
