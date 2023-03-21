from fastapi import APIRouter

from .endpoint import script_api, script_action_api, action_api

api_router = APIRouter(prefix="/v1")

api_router.include_router(script_api.router, prefix="/scripts", tags=["scripts"])
api_router.include_router(script_action_api.router, prefix="/script-actions", tags=["script-actions"])
api_router.include_router(action_api.router, prefix="/actions", tags=["actions"])


