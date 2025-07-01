"""
Coffee and category related schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None
    sortOrder: int = Field(default=0, ge=0)
    active: bool = True


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = None
    description: Optional[str] = None
    sortOrder: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class CoffeeBase(BaseModel):
    """Base coffee schema."""
    name: str = Field(..., example="卡布奇诺")
    description: str = Field(..., example="经典意式咖啡，奶泡绵密")
    price: float = Field(..., gt=0, example=25.00)
    categoryId: str
    available: bool = True
    imageUrl: Optional[str] = Field(None, example="/images/cappuccino.jpg")


class CoffeeCreate(CoffeeBase):
    """Schema for creating a coffee item."""
    pass


class CoffeeUpdate(BaseModel):
    """Schema for updating a coffee item."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    categoryId: Optional[str] = None
    available: Optional[bool] = None
    imageUrl: Optional[str] = None


class CoffeeResponse(CoffeeBase):
    """Coffee response schema."""
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class CoffeeWithCategory(CoffeeResponse):
    """Coffee response with category details."""
    category: CategoryResponse