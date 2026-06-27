
from celery import Celery
from backend.app.core.config import settings

celery = Celery(
    "mlp",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_track_started=True,
)
