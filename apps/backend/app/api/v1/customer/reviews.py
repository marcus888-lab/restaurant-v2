"""
Customer review endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma
from prisma.models import User

from app.core.database import get_db_dependency
from app.core.auth import get_current_user
from app.schemas import (
    StandardResponse,
    ReviewResponse,
    ReviewCreateRequest,
    ReviewUpdateRequest,
    ErrorResponse
)

router = APIRouter(prefix="/reviews", tags=["Customer Reviews"])


@router.post(
    "",
    response_model=StandardResponse[ReviewResponse],
    summary="创建评价",
    description="为咖啡产品创建评价"
)
async def create_review(
    review_data: ReviewCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[ReviewResponse]:
    """Create a new review."""
    try:
        # Check if coffee exists
        coffee = await db.coffee.find_unique(where={"id": review_data.coffeeId})
        if not coffee:
            raise HTTPException(
                status_code=404,
                detail="咖啡产品不存在"
            )
        
        # Check if user has already reviewed this coffee
        existing_review = await db.review.find_first(
            where={
                "userId": current_user.id,
                "coffeeId": review_data.coffeeId
            }
        )
        
        if existing_review:
            raise HTTPException(
                status_code=400,
                detail="您已经评价过此产品"
            )
        
        # Check if user has ordered this coffee
        order_item = await db.orderitem.find_first(
            where={
                "coffeeId": review_data.coffeeId,
                "order": {
                    "userId": current_user.id,
                    "status": {"in": ["COMPLETED"]}
                }
            }
        )
        
        if not order_item:
            raise HTTPException(
                status_code=400,
                detail="只能评价已购买的产品"
            )
        
        # Create review
        review = await db.review.create(
            data={
                "userId": current_user.id,
                "coffeeId": review_data.coffeeId,
                "rating": review_data.rating,
                "comment": review_data.comment
            },
            include={
                "coffee": True,
                "user": True
            }
        )
        
        return StandardResponse(
            success=True,
            data=review,
            message="评价创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建评价失败: {str(e)}"
        )


@router.get(
    "/my",
    response_model=StandardResponse[List[ReviewResponse]],
    summary="获取我的评价",
    description="获取当前用户的所有评价"
)
async def get_my_reviews(
    limit: int = Query(50, ge=1, le=100, description="返回数量限制"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[ReviewResponse]]:
    """Get current user's reviews."""
    try:
        reviews = await db.review.find_many(
            where={"userId": current_user.id},
            include={
                "coffee": {
                    "include": {
                        "category": True
                    }
                }
            },
            order={"createdAt": "desc"},
            take=limit,
            skip=skip
        )
        
        return StandardResponse(
            success=True,
            data=reviews,
            message="获取评价成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取评价失败: {str(e)}"
        )


@router.get(
    "/coffee/{coffee_id}",
    response_model=StandardResponse[List[ReviewResponse]],
    summary="获取产品评价",
    description="获取指定咖啡产品的所有评价"
)
async def get_coffee_reviews(
    coffee_id: str,
    limit: int = Query(50, ge=1, le=100, description="返回数量限制"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[ReviewResponse]]:
    """Get reviews for a specific coffee."""
    try:
        # Check if coffee exists
        coffee = await db.coffee.find_unique(where={"id": coffee_id})
        if not coffee:
            raise HTTPException(
                status_code=404,
                detail="咖啡产品不存在"
            )
        
        reviews = await db.review.find_many(
            where={"coffeeId": coffee_id},
            include={
                "user": True
            },
            order={"createdAt": "desc"},
            take=limit,
            skip=skip
        )
        
        # Calculate average rating
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            message = f"获取评价成功，平均评分: {avg_rating:.1f}"
        else:
            message = "获取评价成功，暂无评价"
        
        return StandardResponse(
            success=True,
            data=reviews,
            message=message
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取评价失败: {str(e)}"
        )


@router.put(
    "/{review_id}",
    response_model=StandardResponse[ReviewResponse],
    summary="更新评价",
    description="更新自己的评价"
)
async def update_review(
    review_id: str,
    review_data: ReviewUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[ReviewResponse]:
    """Update a review."""
    try:
        # Get review
        review = await db.review.find_unique(
            where={"id": review_id}
        )
        
        if not review:
            raise HTTPException(
                status_code=404,
                detail="评价不存在"
            )
        
        # Verify review belongs to current user
        if review.userId != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="无权修改此评价"
            )
        
        # Update review
        updated_review = await db.review.update(
            where={"id": review_id},
            data={
                "rating": review_data.rating,
                "comment": review_data.comment
            },
            include={
                "coffee": True,
                "user": True
            }
        )
        
        return StandardResponse(
            success=True,
            data=updated_review,
            message="评价更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新评价失败: {str(e)}"
        )


@router.delete(
    "/{review_id}",
    response_model=StandardResponse[dict],
    summary="删除评价",
    description="删除自己的评价"
)
async def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Delete a review."""
    try:
        # Get review
        review = await db.review.find_unique(
            where={"id": review_id}
        )
        
        if not review:
            raise HTTPException(
                status_code=404,
                detail="评价不存在"
            )
        
        # Verify review belongs to current user
        if review.userId != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="无权删除此评价"
            )
        
        # Delete review
        await db.review.delete(where={"id": review_id})
        
        return StandardResponse(
            success=True,
            data={"id": review_id},
            message="评价删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除评价失败: {str(e)}"
        )