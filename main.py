from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch, json
import torch.nn as nn
import numpy as np

app = FastAPI(title="Forecast API", version="1.0.0")

# === Load Model + Meta ===
class ForecastGRU(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(1, 32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        h, _ = self.gru(x)
        return self.fc(h[:, -1])

try:
    with open("models/forecast_meta.json") as f:
        meta = json.load(f)
    model = ForecastGRU()
    model.load_state_dict(torch.load("models/forecast.pt", map_location="cpu"))
    model.eval()
except Exception as e:
    raise RuntimeError(f"Model load failed: {e}")

# === Input Schema ===
class ForecastRequest(BaseModel):
    values: list[float]  # must be length 12

@app.get("/health")
def health():
    return {"ok": True, "model": "ForecastGRU", "version": "1.0.0"}

@app.post("/predict")
def predict(req: ForecastRequest):
    try:
        x = np.array(req.values)
        if len(x) != meta["seq_len"]:
            raise HTTPException(status_code=400, detail="Input must be length 12.")
        x = (x - meta["mean"]) / meta["std"]
        x = torch.tensor(x, dtype=torch.float32).reshape(1, -1, 1)
        with torch.no_grad():
            y = model(x).item()
        y = y * meta["std"] + meta["mean"]
        return {"forecast": round(y, 3)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
