from fastapi import APIRouter

from .endpoint import script_api

api_router = APIRouter(prefix="/v1")

api_router.include_router(script_api.router, prefix="/scripts", tags=["scripts"])

