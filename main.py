from fastapi import FastAPI
from datetime import datetime
from utils import generate_forecast

app = FastAPI()

@app.get("/forecast")
async def forecast():
    input_sequence = [100, 110, 120, 115, 125]  # Simulated input
    prediction = generate_forecast(input_sequence)

    return {
        "model": "forecast-lstm-v1.0",
        "status": "online",
        "lastUpdated": str(datetime.utcnow().date()),
        "data": {
            "input": input_sequence,
            "prediction": prediction
        }
    }
