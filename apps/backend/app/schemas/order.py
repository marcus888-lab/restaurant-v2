"""
Order-related schemas.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OrderType(str, Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class CoffeeSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class OrderItemBase(BaseModel):
    """Base order item schema."""
    coffeeId: str
    quantity: int = Field(..., ge=1)
    size: CoffeeSize = CoffeeSize.MEDIUM
    notes: Optional[str] = Field(None, max_length=500)


class OrderItemCreate(OrderItemBase):
    """Schema for creating order items."""
    pass


class OrderItemResponse(OrderItemBase):
    """Order item response schema."""
    id: str
    price: float
    
    model_config = {"from_attributes": True}


class OrderBase(BaseModel):
    """Base order schema."""
    type: OrderType = OrderType.PICKUP
    notes: Optional[str] = Field(None, max_length=1000)


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    items: List[OrderItemCreate] = Field(..., min_items=1)
    type: OrderType = OrderType.PICKUP
    notes: Optional[str] = Field(None, max_length=1000)


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[OrderStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class OrderResponse(BaseModel):
    """Order response schema."""
    id: str
    orderNumber: str
    userId: str
    subtotal: float
    tax: float
    total: float
    status: OrderStatus
    type: OrderType
    items: List[OrderItemResponse] = []
    createdAt: datetime
    updatedAt: datetime
    
    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    """Simplified order for list views."""
    id: str
    orderNumber: str
    total: float
    status: OrderStatus
    type: OrderType
    itemCount: int
    createdAt: datetime
    
    model_config = {"from_attributes": True}


class OrderItemDetailResponse(OrderItemResponse):
    """Order item with coffee details."""
    coffee: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True}


class OrderDetailResponse(OrderResponse):
    """Detailed order response with all relations."""
    user: Optional[Dict[str, Any]] = None
    orderItems: List[OrderItemDetailResponse] = []
    payment: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True}


class OrderCreateRequest(BaseModel):
    """Request for creating an order."""
    items: List['OrderItemRequest'] = Field(..., min_items=1)
    type: OrderType = OrderType.PICKUP
    notes: Optional[str] = Field(None, max_length=1000)


class OrderItemRequest(BaseModel):
    """Individual item in order creation request."""
    coffeeId: str
    quantity: int = Field(..., ge=1)
    size: CoffeeSize = CoffeeSize.MEDIUM
    notes: Optional[str] = Field(None, max_length=500)


class OrderUpdateStatus(BaseModel):
    """Request for updating order status."""
    status: OrderStatus