"""
Admin menu management endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from prisma import Prisma
from prisma.models import User

from app.core.database import get_db_dependency
from app.core.auth import get_current_admin_user
from app.schemas import (
    StandardResponse,
    CategoryResponse,
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CoffeeResponse,
    CoffeeCreateRequest,
    CoffeeUpdateRequest,
    ErrorResponse
)

router = APIRouter(prefix="/menu", tags=["Admin Menu Management"])




@router.post(
    "/categories",
    response_model=StandardResponse[CategoryResponse],
    summary="创建分类",
    description="创建新的咖啡分类"
)
async def create_category(
    category_data: CategoryCreateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[CategoryResponse]:
    """Create a new category."""
    try:
        # Check if category ID already exists
        existing = await db.category.find_unique(where={"id": category_data.id})
        if existing:
            raise HTTPException(
                status_code=400,
                detail="分类ID已存在"
            )
        
        category = await db.category.create(
            data={
                "id": category_data.id,
                "name": category_data.name,
                "description": category_data.description,
                "sortOrder": category_data.sortOrder,
                "active": category_data.active
            }
        )
        
        return StandardResponse(
            success=True,
            data=category,
            message="分类创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建分类失败: {str(e)}"
        )


@router.put(
    "/categories/{category_id}",
    response_model=StandardResponse[CategoryResponse],
    summary="更新分类",
    description="更新咖啡分类信息"
)
async def update_category(
    category_id: str,
    category_data: CategoryUpdateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[CategoryResponse]:
    """Update a category."""
    try:
        # Check if category exists
        existing = await db.category.find_unique(where={"id": category_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="分类不存在"
            )
        
        update_data = {}
        if category_data.name is not None:
            update_data["name"] = category_data.name
        if category_data.description is not None:
            update_data["description"] = category_data.description
        if category_data.sortOrder is not None:
            update_data["sortOrder"] = category_data.sortOrder
        if category_data.active is not None:
            update_data["active"] = category_data.active
        
        category = await db.category.update(
            where={"id": category_id},
            data=update_data
        )
        
        return StandardResponse(
            success=True,
            data=category,
            message="分类更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新分类失败: {str(e)}"
        )


@router.delete(
    "/categories/{category_id}",
    response_model=StandardResponse[dict],
    summary="删除分类",
    description="删除咖啡分类"
)
async def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Delete a category."""
    try:
        # Check if category exists
        existing = await db.category.find_unique(where={"id": category_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="分类不存在"
            )
        
        # Check if category has coffee items
        coffee_count = await db.coffee.count(where={"categoryId": category_id})
        if coffee_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"分类下有 {coffee_count} 个咖啡产品，无法删除"
            )
        
        await db.category.delete(where={"id": category_id})
        
        return StandardResponse(
            success=True,
            data={"id": category_id},
            message="分类删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除分类失败: {str(e)}"
        )


@router.post(
    "/items",
    response_model=StandardResponse[CoffeeResponse],
    summary="创建咖啡产品",
    description="创建新的咖啡产品"
)
async def create_coffee(
    coffee_data: CoffeeCreateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[CoffeeResponse]:
    """Create a new coffee item."""
    try:
        # Check if category exists
        category = await db.category.find_unique(where={"id": coffee_data.categoryId})
        if not category:
            raise HTTPException(
                status_code=400,
                detail="指定的分类不存在"
            )
        
        coffee = await db.coffee.create(
            data={
                "name": coffee_data.name,
                "description": coffee_data.description,
                "price": coffee_data.price,
                "categoryId": coffee_data.categoryId,
                "available": coffee_data.available,
                "imageUrl": coffee_data.imageUrl
            },
            include={"category": True}
        )
        
        return StandardResponse(
            success=True,
            data=coffee,
            message="咖啡产品创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建咖啡产品失败: {str(e)}"
        )


@router.put(
    "/items/{item_id}",
    response_model=StandardResponse[CoffeeResponse],
    summary="更新咖啡产品",
    description="更新咖啡产品信息"
)
async def update_coffee(
    item_id: str,
    coffee_data: CoffeeUpdateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[CoffeeResponse]:
    """Update a coffee item."""
    try:
        # Check if coffee exists
        existing = await db.coffee.find_unique(where={"id": item_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="咖啡产品不存在"
            )
        
        update_data = {}
        if coffee_data.name is not None:
            update_data["name"] = coffee_data.name
        if coffee_data.description is not None:
            update_data["description"] = coffee_data.description
        if coffee_data.price is not None:
            update_data["price"] = coffee_data.price
        if coffee_data.categoryId is not None:
            # Check if new category exists
            category = await db.category.find_unique(where={"id": coffee_data.categoryId})
            if not category:
                raise HTTPException(
                    status_code=400,
                    detail="指定的分类不存在"
                )
            update_data["categoryId"] = coffee_data.categoryId
        if coffee_data.available is not None:
            update_data["available"] = coffee_data.available
        if coffee_data.imageUrl is not None:
            update_data["imageUrl"] = coffee_data.imageUrl
        
        coffee = await db.coffee.update(
            where={"id": item_id},
            data=update_data,
            include={"category": True}
        )
        
        return StandardResponse(
            success=True,
            data=coffee,
            message="咖啡产品更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新咖啡产品失败: {str(e)}"
        )


@router.delete(
    "/items/{item_id}",
    response_model=StandardResponse[dict],
    summary="删除咖啡产品",
    description="删除咖啡产品"
)
async def delete_coffee(
    item_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Prisma = Depends(get_db_dependency)
) -> StandardResponse[dict]:
    """Delete a coffee item."""
    try:
        # Check if coffee exists
        existing = await db.coffee.find_unique(where={"id": item_id})
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="咖啡产品不存在"
            )
        
        # Soft delete by marking as unavailable
        await db.coffee.update(
            where={"id": item_id},
            data={"available": False}
        )
        
        return StandardResponse(
            success=True,
            data={"id": item_id},
            message="咖啡产品已标记为不可用"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除咖啡产品失败: {str(e)}"
        )