"""
Public menu endpoints for coffee items and categories.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma

from app.core.database import get_db_dependency
from app.schemas import (
    StandardResponse,
    CategoryResponse,
    CoffeeResponse,
    CoffeeWithCategory,
    ErrorResponse
)

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get(
    "/categories",
    response_model=StandardResponse[List[CategoryResponse]],
    summary="获取所有分类",
    description="获取所有激活的咖啡分类"
)
async def get_categories(
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[CategoryResponse]]:
    """Get all active categories."""
    try:
        categories = await db.category.find_many(
            where={"active": True},
            order={"sortOrder": "asc"}
        )
        
        return StandardResponse(
            success=True,
            data=categories,
            message="获取分类成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取分类失败: {str(e)}"
        )


@router.get(
    "/items",
    response_model=StandardResponse[List[CoffeeResponse]],
    summary="获取咖啡菜单",
    description="获取所有可用的咖啡项目，可按分类筛选"
)
async def get_menu_items(
    category: Optional[str] = Query(None, description="分类ID筛选"),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[List[CoffeeResponse]]:
    """Get all available coffee items, optionally filtered by category."""
    try:
        where_clause = {"available": True}
        if category:
            where_clause["categoryId"] = category
        
        coffee_items = await db.coffee.find_many(
            where=where_clause,
            order={"name": "asc"}
        )
        
        return StandardResponse(
            success=True,
            data=coffee_items,
            message="获取咖啡菜单成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取咖啡菜单失败: {str(e)}"
        )


@router.get(
    "/items/{item_id}",
    response_model=StandardResponse[CoffeeWithCategory],
    summary="获取单个咖啡详情",
    description="根据ID获取咖啡项目的详细信息"
)
async def get_menu_item(
    item_id: str,
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[CoffeeWithCategory]:
    """Get details of a single coffee item."""
    try:
        coffee_item = await db.coffee.find_unique(
            where={"id": item_id},
            include={"category": True}
        )
        
        if not coffee_item:
            raise HTTPException(
                status_code=404,
                detail="咖啡项目不存在"
            )
        
        if not coffee_item.available:
            raise HTTPException(
                status_code=404,
                detail="咖啡项目暂不可用"
            )
        
        return StandardResponse(
            success=True,
            data=coffee_item,
            message="获取咖啡详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取咖啡详情失败: {str(e)}"
        )