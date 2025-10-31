# tasks.py
from celery import shared_task
import torch, requests, os

MODEL_PATH = "models/forecast.pt"
S3_URL = os.getenv("S3_MODEL_URL", "https://your-bucket.s3.amazonaws.com/models/forecast.pt")

@shared_task
def refresh_model():
    """
    Downloads the latest forecast model weights from S3
    and replaces the local file. Runs daily from Celery Beat.
    """
    try:
        print("[TASK] Refreshing model from S3...")
        r = requests.get(S3_URL, timeout=30)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)
            print("[TASK] Model refreshed successfully.")
        else:
            print(f"[TASK] Failed to download model. Status: {r.status_code}")
    except Exception as e:
        print(f"[TASK] Error refreshing model: {e}")
