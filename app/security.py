import os
from fastapi import Header, HTTPException, status

API_KEY = os.getenv('API_KEY')

async def require_key(x_api_key: str = Header(None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')
