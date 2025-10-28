from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, time

app = FastAPI(title="quant-service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "online", "detail": "ok", "ts": time.time()}
