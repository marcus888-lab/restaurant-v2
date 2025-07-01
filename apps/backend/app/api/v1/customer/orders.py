"""
Customer order endpoints.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma
from prisma.models import User

from app.core.database import get_db_dependency
from app.core.auth import get_current_user
from app.schemas import (
    StandardResponse,
    OrderResponse,
    OrderDetailResponse,
    OrderCreateRequest,
    OrderItemRequest,
    OrderUpdateStatus,
    ErrorResponse
)

router = APIRouter(prefix="/orders", tags=["Customer Orders"])


@router.post(
    "",
    response_model=StandardResponse[OrderResponse],
    summary="创建新订单",
    description="创建新的咖啡订单"
)
async def create_order(
    order_data: OrderCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[OrderResponse]:
    """Create a new order."""
    try:
        # Validate all coffee items exist and are available
        coffee_items = []
        for item in order_data.items:
            coffee = await db.coffee.find_unique(where={"id": item.coffeeId})
            if not coffee:
                raise HTTPException(
                    status_code=400,
                    detail=f"咖啡项目 {item.coffeeId} 不存在"
                )
            if not coffee.available:
                raise HTTPException(
                    status_code=400,
                    detail=f"咖啡项目 {coffee.name} 暂不可用"
                )
            coffee_items.append((coffee, item))
        
        # Calculate totals
        subtotal = sum(coffee.price * item.quantity for coffee, item in coffee_items)
        tax = subtotal * 0.08  # 8% tax
        total = subtotal + tax
        
        # Generate order number
        order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create order with items
        order = await db.order.create(
            data={
                "userId": current_user.id,
                "orderNumber": order_number,
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
                "status": "PENDING",
                "type": order_data.type,
                "orderItems": {
                    "create": [
                        {
                            "coffeeId": coffee.id,
                            "quantity": item.quantity,
                            "price": coffee.price,
                            "size": item.size,
                            "notes": item.notes
                        }
                        for coffee, item in coffee_items
                    ]
                }
            },
            include={
                "orderItems": {
                    "include": {
                        "coffee": True
                    }
                }
            }
        )
        
        # Update user rewards points
        await db.rewards.upsert(
            where={"userId": current_user.id},
            create={
                "userId": current_user.id,
                "currentPoints": int(total),
                "totalEarned": int(total),
                "totalRedeemed": 0
            },
            update={
                "currentPoints": {"increment": int(total)},
                "totalEarned": {"increment": int(total)}
            }
        )
        
        return StandardResponse(
            success=True,
            data=order,
            message="订单创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建订单失败: {str(e)}"
        )


@router.get(
    "",
    response_model=StandardResponse[List[OrderResponse]],
    summary="获取我的订单",
    description="获取当前用户的所有订单"
)
async def get_my_orders(
    status: Optional[str] = Query(None, description="订单状态筛选"),
    limit: int = Query(50, ge=1, le=100, description="返回数量限制"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[OrderResponse]]:
    """Get current user's orders."""
    try:
        where_clause = {"userId": current_user.id}
        if status:
            where_clause["status"] = status
        
        orders = await db.order.find_many(
            where=where_clause,
            include={
                "orderItems": {
                    "include": {
                        "coffee": True
                    }
                }
            },
            order={"createdAt": "desc"},
            take=limit,
            skip=skip
        )
        
        return StandardResponse(
            success=True,
            data=orders,
            message="获取订单成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取订单失败: {str(e)}"
        )


@router.get(
    "/{order_id}",
    response_model=StandardResponse[OrderDetailResponse],
    summary="获取订单详情",
    description="获取指定订单的详细信息"
)
async def get_order_detail(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[OrderDetailResponse]:
    """Get order details."""
    try:
        order = await db.order.find_unique(
            where={"id": order_id},
            include={
                "orderItems": {
                    "include": {
                        "coffee": {
                            "include": {
                                "category": True
                            }
                        }
                    }
                },
                "payment": True,
                "user": True
            }
        )
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail="订单不存在"
            )
        
        # Verify order belongs to current user
        if order.userId != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="无权查看此订单"
            )
        
        return StandardResponse(
            success=True,
            data=order,
            message="获取订单详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取订单详情失败: {str(e)}"
        )


@router.patch(
    "/{order_id}/cancel",
    response_model=StandardResponse[OrderResponse],
    summary="取消订单",
    description="取消待处理的订单"
)
async def cancel_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[OrderResponse]:
    """Cancel a pending order."""
    try:
        # Get order
        order = await db.order.find_unique(
            where={"id": order_id}
        )
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail="订单不存在"
            )
        
        # Verify order belongs to current user
        if order.userId != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="无权取消此订单"
            )
        
        # Check if order can be cancelled
        if order.status not in ["PENDING", "CONFIRMED"]:
            raise HTTPException(
                status_code=400,
                detail=f"订单状态为 {order.status}，无法取消"
            )
        
        # Update order status
        updated_order = await db.order.update(
            where={"id": order_id},
            data={"status": "CANCELLED"},
            include={
                "orderItems": {
                    "include": {
                        "coffee": True
                    }
                }
            }
        )
        
        # Deduct rewards points if order was paid
        if order.status == "CONFIRMED":
            await db.rewards.update(
                where={"userId": current_user.id},
                data={
                    "currentPoints": {"decrement": int(order.total)},
                    "totalEarned": {"decrement": int(order.total)}
                }
            )
        
        return StandardResponse(
            success=True,
            data=updated_order,
            message="订单已取消"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"取消订单失败: {str(e)}"
        )