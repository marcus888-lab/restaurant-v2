"""
Customer API routes.
"""
from fastapi import APIRouter
from .orders import router as orders_router
from .reviews import router as reviews_router
from .rewards import router as rewards_router

router = APIRouter()

router.include_router(orders_router)
router.include_router(reviews_router)
router.include_router(rewards_router)