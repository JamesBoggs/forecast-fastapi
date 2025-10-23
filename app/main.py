# app/main.py
from fastapi import FastAPI

# create the app FIRST
app = FastAPI()

# now import routers/middleware helpers
from app.routes.health import router as health_router
from app.routes.metrics import router as metrics_router
from app.limiting import add_rate_limit
from app.middlewares import BodySizeLimitMiddleware
from app.bootstrap import apply_bootstrap
from app.logging_redact import install_redaction

# wire routes
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])

# security/middleware
app.add_middleware(BodySizeLimitMiddleware, max_body=1_000_000)
add_rate_limit(app)
app = apply_bootstrap(app, allowed_origins=["https://jamesboggs.online"])
install_redaction()
