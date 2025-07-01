"""
Customer rewards endpoints.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from prisma.models import User

from app.core.database import get_db_dependency
from app.core.auth import get_current_user
from app.schemas import (
    StandardResponse,
    RewardsResponse,
    RewardsHistoryResponse,
    RewardsRedeemRequest,
    ErrorResponse
)

router = APIRouter(prefix="/rewards", tags=["Customer Rewards"])


@router.get(
    "/my",
    response_model=StandardResponse[RewardsResponse],
    summary="获取我的积分",
    description="获取当前用户的积分信息"
)
async def get_my_rewards(
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[RewardsResponse]:
    """Get current user's rewards information."""
    try:
        rewards = await db.rewards.find_unique(
            where={"userId": current_user.id},
            include={"user": True}
        )
        
        if not rewards:
            # Create rewards record if doesn't exist
            rewards = await db.rewards.create(
                data={
                    "userId": current_user.id,
                    "currentPoints": 0,
                    "totalEarned": 0,
                    "totalRedeemed": 0
                },
                include={"user": True}
            )
        
        return StandardResponse(
            success=True,
            data=rewards,
            message="获取积分信息成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取积分信息失败: {str(e)}"
        )


@router.get(
    "/history",
    response_model=StandardResponse[List[dict]],
    summary="获取积分历史",
    description="获取积分获取和使用历史"
)
async def get_rewards_history(
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[dict]]:
    """Get rewards history (earned and redeemed)."""
    try:
        # Get orders that earned points
        completed_orders = await db.order.find_many(
            where={
                "userId": current_user.id,
                "status": {"in": ["COMPLETED"]}
            },
            order={"createdAt": "desc"},
            take=20
        )
        
        history = []
        
        # Add earned points from orders
        for order in completed_orders:
            history.append({
                "type": "EARNED",
                "points": int(order.total),
                "description": f"订单 {order.orderNumber}",
                "date": order.createdAt,
                "orderId": order.id
            })
        
        # Sort by date
        history.sort(key=lambda x: x["date"], reverse=True)
        
        return StandardResponse(
            success=True,
            data=history,
            message="获取积分历史成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取积分历史失败: {str(e)}"
        )


@router.post(
    "/redeem",
    response_model=StandardResponse[dict],
    summary="兑换积分",
    description="使用积分兑换免费咖啡"
)
async def redeem_rewards(
    redeem_data: RewardsRedeemRequest,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Redeem rewards points for free coffee."""
    try:
        # Get user rewards
        rewards = await db.rewards.find_unique(
            where={"userId": current_user.id}
        )
        
        if not rewards:
            raise HTTPException(
                status_code=400,
                detail="您还没有积分"
            )
        
        # Check points requirement
        points_required = 200  # 200 points for free coffee
        
        if rewards.currentPoints < points_required:
            raise HTTPException(
                status_code=400,
                detail=f"积分不足，需要 {points_required} 积分，当前有 {rewards.currentPoints} 积分"
            )
        
        # Check if coffee exists
        coffee = await db.coffee.find_unique(where={"id": redeem_data.coffeeId})
        if not coffee:
            raise HTTPException(
                status_code=404,
                detail="咖啡产品不存在"
            )
        
        if not coffee.available:
            raise HTTPException(
                status_code=400,
                detail="该咖啡产品暂不可用"
            )
        
        # Create redemption order
        order_number = f"RWD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        order = await db.order.create(
            data={
                "userId": current_user.id,
                "orderNumber": order_number,
                "subtotal": 0,
                "tax": 0,
                "total": 0,
                "status": "CONFIRMED",
                "type": "PICKUP",
                "orderItems": {
                    "create": [{
                        "coffeeId": coffee.id,
                        "quantity": 1,
                        "price": 0,
                        "size": redeem_data.size,
                        "notes": "积分兑换"
                    }]
                }
            }
        )
        
        # Update rewards
        await db.rewards.update(
            where={"userId": current_user.id},
            data={
                "currentPoints": {"decrement": points_required},
                "totalRedeemed": {"increment": points_required}
            }
        )
        
        return StandardResponse(
            success=True,
            data={
                "orderId": order.id,
                "orderNumber": order.orderNumber,
                "coffeeId": coffee.id,
                "coffeeName": coffee.name,
                "pointsUsed": points_required,
                "remainingPoints": rewards.currentPoints - points_required
            },
            message=f"成功兑换 {coffee.name}，使用了 {points_required} 积分"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"兑换积分失败: {str(e)}"
        )


@router.get(
    "/benefits",
    response_model=StandardResponse[dict],
    summary="获取会员权益",
    description="获取会员等级和权益信息"
)
async def get_rewards_benefits(
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Get member benefits and tier information."""
    try:
        rewards = await db.rewards.find_unique(
            where={"userId": current_user.id}
        )
        
        if not rewards:
            rewards = await db.rewards.create(
                data={
                    "userId": current_user.id,
                    "currentPoints": 0,
                    "totalEarned": 0,
                    "totalRedeemed": 0
                }
            )
        
        # Calculate member tier based on total earned
        total_earned = rewards.totalEarned
        
        if total_earned >= 5000:
            tier = "GOLD"
            tier_name = "金卡会员"
            benefits = [
                "每笔消费获得1.5倍积分",
                "200积分兑换免费咖啡",
                "生日当月双倍积分",
                "专属会员活动"
            ]
            next_tier_points = None
        elif total_earned >= 2000:
            tier = "SILVER"
            tier_name = "银卡会员"
            benefits = [
                "每笔消费获得1.2倍积分",
                "200积分兑换免费咖啡",
                "生日当月1.5倍积分"
            ]
            next_tier_points = 5000 - total_earned
        else:
            tier = "BRONZE"
            tier_name = "铜卡会员"
            benefits = [
                "每笔消费获得1倍积分",
                "200积分兑换免费咖啡"
            ]
            next_tier_points = 2000 - total_earned
        
        return StandardResponse(
            success=True,
            data={
                "tier": tier,
                "tierName": tier_name,
                "currentPoints": rewards.currentPoints,
                "totalEarned": rewards.totalEarned,
                "benefits": benefits,
                "nextTierPoints": next_tier_points,
                "redemptionInfo": {
                    "pointsRequired": 200,
                    "canRedeem": rewards.currentPoints >= 200
                }
            },
            message="获取会员权益成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取会员权益失败: {str(e)}"
        )