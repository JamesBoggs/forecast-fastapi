from fastapi import APIRouter
import time, platform, os
import torch

router = APIRouter()

def _model():
    from app.model import model
    return model

def _dummy():
    return torch.zeros(1, 24, 8)(dtype=torch.float32)

@router.get('/')
def health():
    m = _model()
    ok = True
    err = None
    t0 = time.perf_counter()
    try:
        with torch.no_grad():
            _ = m(_dummy())
    except Exception as e:
        ok, err = False, str(e)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    return {
        "ok": ok,
        "error": err,
        "trained": os.path.exists("models/forecast.pt"),
        "weights_format": ".pt",
        "weights_uri": "models/forecast.pt",
        "latency_ms": round(dt_ms, 2),
        "torch": torch.__version__,
        "cuda": getattr(torch.version, "cuda", None),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "python": platform.python_version(),
        "host": platform.node(),
        "last_updated": "2025-10-23T01:16:42.714510"
    }
