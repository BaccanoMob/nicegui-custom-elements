from nicegui import app, ui
from starlette.middleware.sessions import SessionMiddleware

from app.web import examples

## METHOD TO ADD SECURE SESSION COOKIES
app.add_middleware(
    SessionMiddleware, secret_key="my_secret", same_site="strict", https_only=True
)

## Adding routers
app.include_router(examples.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=8000,
        reload=True,
        show=False,
        storage_secret="my_secret",  # SAME SECRET AS ABOVE
    )
