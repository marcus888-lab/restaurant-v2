"""
API v1 routes.
"""
from fastapi import APIRouter

from app.api.v1.public import menu
from app.api.v1.auth import auth
from app.api.v1.customer import orders, reviews, rewards
from app.api.v1.admin import menu_management, analytics, orders_management

# Create main API router
api_router = APIRouter()

# Include public routes
api_router.include_router(menu.router, prefix="/api/v1")

# Include auth routes
api_router.include_router(auth.router, prefix="/api/v1")

# Include customer routes (protected)
api_router.include_router(orders.router, prefix="/api/v1/customer")
api_router.include_router(reviews.router, prefix="/api/v1/customer")
api_router.include_router(rewards.router, prefix="/api/v1/customer")

# Include admin routes (protected)
api_router.include_router(menu_management.router, prefix="/api/v1/admin")
api_router.include_router(analytics.router, prefix="/api/v1/admin")
api_router.include_router(orders_management.router, prefix="/api/v1/admin")