from fastapi import Request
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app import create_app
from dashapp import create_dash_app
from routers import dashboard, operation

app = create_app()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

app.include_router(dashboard.router)
app.include_router(operation.router)

dash_app = create_dash_app(requests_pathname_prefix="/dash/")
app.mount("/dash", WSGIMiddleware(dash_app.server))

add_pagination(app)
