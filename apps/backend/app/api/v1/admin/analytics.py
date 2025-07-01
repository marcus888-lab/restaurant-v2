"""
Admin analytics endpoints.
"""
from typing import List, Optional
from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma
from prisma.models import Order, User

from app.core.database import get_db_dependency
from app.core.auth import get_current_admin_user
from app.schemas import StandardResponse, ErrorResponse

router = APIRouter(prefix="/analytics", tags=["Admin Analytics"])




@router.get(
    "/overview",
    response_model=StandardResponse[dict],
    summary="获取总览数据",
    description="获取销售总览和关键指标"
)
async def get_overview(
    period: str = Query("today", description="时间段: today, week, month, year"),
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Get overview analytics."""
    try:
        # Calculate date range
        now = datetime.now()
        if period == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "year":
            start_date = now - timedelta(days=365)
        else:
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get orders in period
        orders = await db.order.find_many(
            where={
                "createdAt": {"gte": start_date},
                "status": {"in": ["COMPLETED"]}
            }
        )
        
        # Calculate metrics
        total_revenue = sum(order.total for order in orders)
        total_orders = len(orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Get previous period for comparison
        if period == "today":
            prev_start = start_date - timedelta(days=1)
            prev_end = start_date
        elif period == "week":
            prev_start = start_date - timedelta(days=7)
            prev_end = start_date
        elif period == "month":
            prev_start = start_date - timedelta(days=30)
            prev_end = start_date
        else:
            prev_start = start_date - timedelta(days=365)
            prev_end = start_date
        
        prev_orders = await db.order.find_many(
            where={
                "createdAt": {"gte": prev_start, "lt": prev_end},
                "status": {"in": ["COMPLETED"]}
            }
        )
        
        prev_revenue = sum(order.total for order in prev_orders)
        revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        
        # Get customer count
        unique_customers = set(order.userId for order in orders)
        customer_count = len(unique_customers)
        
        # Get top selling items
        order_items = []
        for order in orders:
            items = await db.orderitem.find_many(
                where={"orderId": order.id},
                include={"coffee": True}
            )
            order_items.extend(items)
        
        # Count coffee sales
        coffee_sales = {}
        for item in order_items:
            coffee_name = item.coffee.name
            if coffee_name not in coffee_sales:
                coffee_sales[coffee_name] = {"quantity": 0, "revenue": 0}
            coffee_sales[coffee_name]["quantity"] += item.quantity
            coffee_sales[coffee_name]["revenue"] += item.price * item.quantity
        
        # Sort by quantity
        top_items = sorted(
            [(name, data) for name, data in coffee_sales.items()],
            key=lambda x: x[1]["quantity"],
            reverse=True
        )[:5]
        
        return StandardResponse(
            success=True,
            data={
                "period": period,
                "revenue": {
                    "total": total_revenue,
                    "change": revenue_change,
                    "currency": "CNY"
                },
                "orders": {
                    "total": total_orders,
                    "avgValue": avg_order_value
                },
                "customers": {
                    "active": customer_count
                },
                "topItems": [
                    {
                        "name": name,
                        "quantity": data["quantity"],
                        "revenue": data["revenue"]
                    }
                    for name, data in top_items
                ]
            },
            message="获取总览数据成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取总览数据失败: {str(e)}"
        )


@router.get(
    "/sales",
    response_model=StandardResponse[dict],
    summary="获取销售数据",
    description="获取详细销售数据和趋势"
)
async def get_sales_data(
    days: int = Query(30, description="天数"),
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Get sales data and trends."""
    try:
        # Get daily sales for the period
        start_date = datetime.now() - timedelta(days=days)
        
        orders = await db.order.find_many(
            where={
                "createdAt": {"gte": start_date},
                "status": {"in": ["COMPLETED"]}
            },
            order={"createdAt": "asc"}
        )
        
        # Group by date
        daily_sales = {}
        for order in orders:
            date_key = order.createdAt.date()
            if date_key not in daily_sales:
                daily_sales[date_key] = {"revenue": 0, "orders": 0}
            daily_sales[date_key]["revenue"] += order.total
            daily_sales[date_key]["orders"] += 1
        
        # Fill in missing dates
        current_date = start_date.date()
        end_date = datetime.now().date()
        all_dates = []
        
        while current_date <= end_date:
            if current_date not in daily_sales:
                daily_sales[current_date] = {"revenue": 0, "orders": 0}
            all_dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Sort by date
        sorted_sales = [
            {
                "date": date.isoformat(),
                "revenue": daily_sales[date]["revenue"],
                "orders": daily_sales[date]["orders"]
            }
            for date in sorted(all_dates)
        ]
        
        # Calculate totals
        total_revenue = sum(day["revenue"] for day in sorted_sales)
        total_orders = sum(day["orders"] for day in sorted_sales)
        
        return StandardResponse(
            success=True,
            data={
                "daily": sorted_sales,
                "summary": {
                    "totalRevenue": total_revenue,
                    "totalOrders": total_orders,
                    "avgDailyRevenue": total_revenue / len(sorted_sales) if sorted_sales else 0,
                    "avgDailyOrders": total_orders / len(sorted_sales) if sorted_sales else 0
                }
            },
            message="获取销售数据成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取销售数据失败: {str(e)}"
        )


@router.get(
    "/products",
    response_model=StandardResponse[List[dict]],
    summary="获取产品销售数据",
    description="获取各产品的销售情况"
)
async def get_product_analytics(
    days: int = Query(30, description="天数"),
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[dict]]:
    """Get product sales analytics."""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        # Get completed orders
        orders = await db.order.find_many(
            where={
                "createdAt": {"gte": start_date},
                "status": {"in": ["COMPLETED"]}
            }
        )
        
        # Get all order items
        product_stats = {}
        
        for order in orders:
            items = await db.orderitem.find_many(
                where={"orderId": order.id},
                include={
                    "coffee": {
                        "include": {"category": True}
                    }
                }
            )
            
            for item in items:
                coffee_id = item.coffeeId
                if coffee_id not in product_stats:
                    product_stats[coffee_id] = {
                        "id": coffee_id,
                        "name": item.coffee.name,
                        "category": item.coffee.category.name,
                        "price": item.coffee.price,
                        "quantity": 0,
                        "revenue": 0,
                        "orders": 0
                    }
                
                product_stats[coffee_id]["quantity"] += item.quantity
                product_stats[coffee_id]["revenue"] += item.price * item.quantity
                product_stats[coffee_id]["orders"] += 1
        
        # Sort by revenue
        sorted_products = sorted(
            product_stats.values(),
            key=lambda x: x["revenue"],
            reverse=True
        )
        
        return StandardResponse(
            success=True,
            data=sorted_products,
            message="获取产品销售数据成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取产品销售数据失败: {str(e)}"
        )


@router.get(
    "/customers",
    response_model=StandardResponse[dict],
    summary="获取客户分析",
    description="获取客户行为和统计数据"
)
async def get_customer_analytics(
    days: int = Query(30, description="天数"),
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Get customer analytics."""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        # Get all users with orders
        users_with_orders = await db.user.find_many(
            where={
                "orders": {
                    "some": {
                        "createdAt": {"gte": start_date}
                    }
                }
            },
            include={
                "orders": {
                    "where": {
                        "createdAt": {"gte": start_date},
                        "status": {"in": ["COMPLETED"]}
                    }
                },
                "rewards": True
            }
        )
        
        # Calculate customer metrics
        total_customers = len(users_with_orders)
        new_customers = sum(1 for user in users_with_orders if user.createdAt >= start_date)
        
        # Customer value distribution
        customer_values = []
        for user in users_with_orders:
            total_spent = sum(order.total for order in user.orders)
            customer_values.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "totalSpent": total_spent,
                "orderCount": len(user.orders),
                "avgOrderValue": total_spent / len(user.orders) if user.orders else 0,
                "rewardPoints": user.rewards.currentPoints if user.rewards else 0
            })
        
        # Sort by total spent
        top_customers = sorted(customer_values, key=lambda x: x["totalSpent"], reverse=True)[:10]
        
        # Calculate segments
        segments = {
            "new": new_customers,
            "regular": sum(1 for cv in customer_values if cv["orderCount"] >= 3),
            "vip": sum(1 for cv in customer_values if cv["totalSpent"] >= 500)
        }
        
        return StandardResponse(
            success=True,
            data={
                "summary": {
                    "totalCustomers": total_customers,
                    "newCustomers": new_customers,
                    "avgCustomerValue": sum(cv["totalSpent"] for cv in customer_values) / total_customers if total_customers > 0 else 0
                },
                "segments": segments,
                "topCustomers": top_customers
            },
            message="获取客户分析成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取客户分析失败: {str(e)}"
        )