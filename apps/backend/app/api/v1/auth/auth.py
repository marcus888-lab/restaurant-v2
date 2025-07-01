"""
Authentication endpoints for user information and token verification.
"""
from fastapi import APIRouter, Depends
from prisma.models import User

from app.core.auth import get_current_user
from app.schemas import StandardResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/me",
    response_model=StandardResponse[UserResponse],
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> StandardResponse[UserResponse]:
    """Get current authenticated user information."""
    return StandardResponse(
        success=True,
        data=current_user,
        message="获取用户信息成功"
    )


@router.get(
    "/verify",
    response_model=StandardResponse[dict],
    summary="验证令牌",
    description="验证当前JWT令牌是否有效"
)
async def verify_token(
    current_user: User = Depends(get_current_user)
) -> StandardResponse[dict]:
    """Verify if the current JWT token is valid."""
    return StandardResponse(
        success=True,
        data={
            "valid": True,
            "userId": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        },
        message="令牌有效"
    )