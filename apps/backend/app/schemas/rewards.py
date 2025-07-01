"""
Rewards-related schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RewardsBase(BaseModel):
    """Base rewards schema."""
    currentPoints: int = Field(default=0, ge=0)
    totalEarned: int = Field(default=0, ge=0)
    totalRedeemed: int = Field(default=0, ge=0)


class RewardsCreate(RewardsBase):
    """Schema for creating rewards record."""
    userId: str


class RewardsUpdate(BaseModel):
    """Schema for updating rewards."""
    currentPoints: Optional[int] = Field(None, ge=0)
    totalEarned: Optional[int] = Field(None, ge=0)
    totalRedeemed: Optional[int] = Field(None, ge=0)


class RewardsResponse(RewardsBase):
    """Rewards response schema."""
    id: str
    userId: str
    lastUpdated: datetime
    
    class Config:
        from_attributes = True


class RewardsTransaction(BaseModel):
    """Schema for rewards transaction."""
    points: int
    type: str = Field(..., pattern="^(EARNED|REDEEMED)$")
    description: str
    orderId: Optional[str] = None