from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse

class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body: int = 1_000_000):
        super().__init__(app); self.max_body = max_body
    async def dispatch(self, request, call_next):
        cl = request.headers.get('content-length')
        if cl and int(cl) > self.max_body:
            return PlainTextResponse('payload too large', status_code=413)
        return await call_next(request)
