from celery import Celery
from core.config import settings

# Inicializamos la instancia de Celery usando las variables de entorno centralizadas
celery_app = Celery(
    "mora_worker",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)