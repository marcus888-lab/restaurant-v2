"""
Admin order management endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma
from prisma.models import User

from app.core.database import get_db_dependency
from app.core.auth import get_current_admin_user
from app.schemas import (
    StandardResponse,
    OrderResponse,
    OrderDetailResponse,
    OrderUpdateStatus,
    ErrorResponse
)

router = APIRouter(prefix="/orders", tags=["Admin Order Management"])




@router.get(
    "",
    response_model=StandardResponse[List[OrderResponse]],
    summary="获取所有订单",
    description="获取所有订单，支持筛选和分页"
)
async def get_all_orders(
    status: Optional[str] = Query(None, description="订单状态筛选"),
    type: Optional[str] = Query(None, description="订单类型筛选"),
    user_id: Optional[str] = Query(None, description="用户ID筛选"),
    limit: int = Query(50, ge=1, le=100, description="返回数量限制"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[OrderResponse]]:
    """Get all orders with filters."""
    try:
        where_clause = {}
        if status:
            where_clause["status"] = status
        if type:
            where_clause["type"] = type
        if user_id:
            where_clause["userId"] = user_id
        
        orders = await db.order.find_many(
            where=where_clause,
            include={
                "orderItems": {
                    "include": {
                        "coffee": True
                    }
                },
                "user": True,
                "payment": True
            },
            order={"createdAt": "desc"},
            take=limit,
            skip=skip
        )
        
        return StandardResponse(
            success=True,
            data=orders,
            message="获取订单列表成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取订单列表失败: {str(e)}"
        )


@router.get(
    "/{order_id}",
    response_model=StandardResponse[OrderDetailResponse],
    summary="获取订单详情",
    description="获取指定订单的详细信息"
)
async def get_order_detail(
    order_id: str,
    current_user: User = Depends(get_current_admin_user),
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
    "/{order_id}/status",
    response_model=StandardResponse[OrderResponse],
    summary="更新订单状态",
    description="更新订单的状态"
)
async def update_order_status(
    order_id: str,
    status_update: OrderUpdateStatus,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[OrderResponse]:
    """Update order status."""
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
        
        # Validate status transition
        valid_transitions = {
            "PENDING": ["CONFIRMED", "CANCELLED"],
            "CONFIRMED": ["PREPARING", "CANCELLED"],
            "PREPARING": ["READY", "CANCELLED"],
            "READY": ["COMPLETED", "CANCELLED"],
            "COMPLETED": [],
            "CANCELLED": []
        }
        
        if status_update.status not in valid_transitions.get(order.status, []):
            raise HTTPException(
                status_code=400,
                detail=f"无法从 {order.status} 状态转换到 {status_update.status} 状态"
            )
        
        # Update order
        updated_order = await db.order.update(
            where={"id": order_id},
            data={"status": status_update.status},
            include={
                "orderItems": {
                    "include": {
                        "coffee": True
                    }
                },
                "user": True
            }
        )
        
        # If order is completed, update rewards
        if status_update.status == "COMPLETED" and order.status != "COMPLETED":
            await db.rewards.upsert(
                where={"userId": order.userId},
                create={
                    "userId": order.userId,
                    "currentPoints": int(order.total),
                    "totalEarned": int(order.total),
                    "totalRedeemed": 0
                },
                update={
                    "currentPoints": {"increment": int(order.total)},
                    "totalEarned": {"increment": int(order.total)}
                }
            )
        
        # If order is cancelled and was confirmed, deduct rewards
        if status_update.status == "CANCELLED" and order.status in ["CONFIRMED", "PREPARING", "READY"]:
            await db.rewards.update(
                where={"userId": order.userId},
                data={
                    "currentPoints": {"decrement": int(order.total)},
                    "totalEarned": {"decrement": int(order.total)}
                }
            )
        
        return StandardResponse(
            success=True,
            data=updated_order,
            message=f"订单状态已更新为 {status_update.status}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新订单状态失败: {str(e)}"
        )


@router.get(
    "/pending/count",
    response_model=StandardResponse[dict],
    summary="获取待处理订单数",
    description="获取各状态的待处理订单数量"
)
async def get_pending_orders_count(
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Get count of pending orders by status."""
    try:
        pending_count = await db.order.count(where={"status": "PENDING"})
        confirmed_count = await db.order.count(where={"status": "CONFIRMED"})
        preparing_count = await db.order.count(where={"status": "PREPARING"})
        ready_count = await db.order.count(where={"status": "READY"})
        
        return StandardResponse(
            success=True,
            data={
                "pending": pending_count,
                "confirmed": confirmed_count,
                "preparing": preparing_count,
                "ready": ready_count,
                "total": pending_count + confirmed_count + preparing_count + ready_count
            },
            message="获取待处理订单数成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取待处理订单数失败: {str(e)}"
        )