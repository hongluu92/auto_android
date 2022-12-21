from fastapi.routing import APIRouter

from auto_mobile.web.api import docs, monitoring
from auto_mobile.web.api.api_v1 import api

api_router = APIRouter()
api_router.include_router(api.api_router)
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
