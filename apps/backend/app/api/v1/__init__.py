"""
API v1 routes.
"""
from fastapi import APIRouter

from app.api.v1.public import menu
from app.api.v1.auth import auth

# Create main API router
api_router = APIRouter()

# Include public routes
api_router.include_router(menu.router, prefix="/api/v1")

# Include auth routes
api_router.include_router(auth.router, prefix="/api/v1")