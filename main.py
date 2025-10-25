# app/main.py
from fastapi import FastAPI
import os, uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "online"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
