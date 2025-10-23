from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse

limiter = Limiter(key_func=get_remote_address)

def add_rate_limit(app):
    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    def ratelimit_handler(request, exc):
        return PlainTextResponse('rate limit', status_code=429)
