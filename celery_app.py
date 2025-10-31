# celery_app.py
from celery import Celery
import os

# === Celery configuration ===
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "forecast_tasks",
    broker=redis_url,
    backend=redis_url,
)

celery_app.conf.timezone = "UTC"

# Beat schedule: runs once every 24 hours
celery_app.conf.beat_schedule = {
    "refresh-model-daily": {
        "task": "tasks.refresh_model",
        "schedule": 24 * 60 * 60,  # every 24 hours
    },
}

@celery_app.task
def test_task():
    print("Celery worker running fine.")
