from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles

from auto_mobile.logging import configure_logging
from auto_mobile.web.api.router import api_router
from auto_mobile.web.lifetime import register_shutdown_event, register_startup_event
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="auto_mobile",
        version=metadata.version("auto_mobile"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        debug=True
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=418,
            content={"message":  "{}".format(exc.__class__.__name__)},
        )

    return app
