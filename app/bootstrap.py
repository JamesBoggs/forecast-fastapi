from fastapi.middleware.cors import CORSMiddleware

def apply_bootstrap(app, allowed_origins=None):
    allowed = allowed_origins or ['https://jamesboggs.online']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed,
        allow_methods=['POST','GET','OPTIONS'],
        allow_headers=['content-type','x-api-key'],
        max_age=600,
    )

    @app.middleware('http')
    async def security_headers(request, call_next):
        r = await call_next(request)
        r.headers['X-Content-Type-Options'] = 'nosniff'
        r.headers['X-Frame-Options'] = 'DENY'
        r.headers['Referrer-Policy'] = 'no-referrer'
        r.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return r

    return app
