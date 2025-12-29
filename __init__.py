import asyncio

from fastapi import APIRouter
from loguru import logger

from .crud import db
from .views import fiatbridge_generic_router
from .views_api import fiatbridge_api_router

fiatbridge_ext = APIRouter(prefix="/fiatbridge", tags=["Fiat Bridge"])
fiatbridge_ext.include_router(fiatbridge_generic_router)
fiatbridge_ext.include_router(fiatbridge_api_router)

fiatbridge_static_files = [
    {
        "path": "/fiatbridge/static",
        "name": "fiatbridge_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []

def fiatbridge_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)

def fiatbridge_start():
    # Background tasks can be added here
    pass

__all__ = [
    "db",
    "fiatbridge_ext",
    "fiatbridge_start",
    "fiatbridge_static_files",
    "fiatbridge_stop",
]
