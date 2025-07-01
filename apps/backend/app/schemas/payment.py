"""
Payment-related schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    ALIPAY = "ALIPAY"
    WECHAT_PAY = "WECHAT_PAY"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentBase(BaseModel):
    """Base payment schema."""
    amount: float = Field(..., gt=0)
    method: PaymentMethod
    transactionId: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Schema for creating a payment."""
    orderId: str


class PaymentUpdate(BaseModel):
    """Schema for updating a payment."""
    status: PaymentStatus
    transactionId: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Payment response schema."""
    id: str
    orderId: str
    status: PaymentStatus
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True