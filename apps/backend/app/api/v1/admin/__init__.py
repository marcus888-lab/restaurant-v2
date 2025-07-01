"""
Admin API routes.
"""
from fastapi import APIRouter
from .menu_management import router as menu_router
from .analytics import router as analytics_router
from .orders_management import router as orders_router

router = APIRouter()

router.include_router(menu_router)
router.include_router(analytics_router)
router.include_router(orders_router)