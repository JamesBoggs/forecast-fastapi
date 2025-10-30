from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import torch, json, os, math, random

# === App Initialization ===
app = FastAPI(title="Forecast Model API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Model + Metadata (Placeholder) ===
MODEL_PATH = "models/forecast.pt"
META_PATH = "models/forecast_meta.json"

model_info = {"model": "Forecast GRU", "framework": "PyTorch", "device": "CPU"}

# Load dummy weights for now
try:
    weights = torch.load(MODEL_PATH, map_location="cpu")
    model_info.update({"weights_loaded": True})
except Exception:
    model_info.update({"weights_loaded": False})


# === Request Schema ===
class ForecastRequest(BaseModel):
    horizon: int = 30
    last_value: float = 100.0
    noise: float = 0.02


# === Routes ===

@app.get("/ping")
def ping():
    """Used by jamesboggs.online dashboard for health check."""
    return {"status": "online"}


@app.post("/simulate")
def simulate(req: ForecastRequest):
    """Generate placeholder forecast values."""
    try:
        preds = []
        value = req.last_value
        for t in range(req.horizon):
            # Dummy logic: smooth trend + random noise
            value += value * random.uniform(-req.noise, req.noise)
            preds.append({"t": t, "y": round(value, 2)})

        # Placeholder for your 7 dashboard tiles
        metrics = {
            "Tile 1": random.uniform(0, 1),
            "Tile 2": random.uniform(0, 1),
            "Tile 3": random.uniform(0, 1),
            "Tile 4": random.uniform(0, 1),
            "Tile 5": random.uniform(0, 1),
            "Tile 6": random.uniform(0, 1),
            "Tile 7": random.uniform(0, 1),
        }

        return {"forecast": preds, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")


@app.get("/meta")
def meta():
    """Optional metadata endpoint (not used by dashboard)."""
    return model_info


# === Root Route ===
@app.get("/")
def root():
    return {
        "message": "Forecast Model API active",
        "routes": ["/ping", "/simulate", "/meta"],
        "model": model_info,
    }
