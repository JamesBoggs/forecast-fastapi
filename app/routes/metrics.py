from fastapi import APIRouter
import threading, time
from collections import deque

router = APIRouter()

_lock = threading.Lock()
_hist = deque(maxlen=256)
errors = 0
calls = 0

def record(lat_ms: float, ok: bool):
    global calls, errors
    with _lock:
        calls += 1
        if not ok:
            errors += 1
        _hist.append(lat_ms)

def _percentile(data, p):
    if not data: return None
    s = sorted(data)
    k = int((len(s)-1) * p)
    return s[k]

@router.get('/')
def metrics():
    with _lock:
        data = list(_hist)
        p50 = _percentile(data, 0.50)
        p95 = _percentile(data, 0.95)
        err_rate = (errors / calls) if calls else 0.0
    return { 'calls': calls, 'errors': errors, 'error_rate': round(err_rate,4),
             'p50_ms': p50, 'p95_ms': p95, 'window': len(data) }
