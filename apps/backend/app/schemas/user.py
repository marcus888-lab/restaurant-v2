"""
User-related schemas.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    clerkId: str
    role: UserRole = UserRole.CUSTOMER


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: str
    role: UserRole
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """User schema with all database fields."""
    clerkId: str