"""
Pydantic schemas for API request/response models.
"""
from .base import (
    StandardResponse,
    ErrorResponse,
    PaginationParams,
    PaginatedResponse
)
from .user import (
    UserRole,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB
)
from .coffee import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CoffeeBase,
    CoffeeCreate,
    CoffeeUpdate,
    CoffeeResponse,
    CoffeeWithCategory
)
from .order import (
    OrderStatus,
    OrderType,
    CoffeeSize,
    OrderItemBase,
    OrderItemCreate,
    OrderItemResponse,
    OrderBase,
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse
)
from .review import (
    ReviewBase,
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewWithUser
)
from .rewards import (
    RewardsBase,
    RewardsCreate,
    RewardsUpdate,
    RewardsResponse,
    RewardsTransaction
)
from .payment import (
    PaymentMethod,
    PaymentStatus,
    PaymentBase,
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse
)

__all__ = [
    # Base
    "StandardResponse",
    "ErrorResponse",
    "PaginationParams",
    "PaginatedResponse",
    # User
    "UserRole",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInDB",
    # Coffee
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "CoffeeBase",
    "CoffeeCreate",
    "CoffeeUpdate",
    "CoffeeResponse",
    "CoffeeWithCategory",
    # Order
    "OrderStatus",
    "OrderType",
    "CoffeeSize",
    "OrderItemBase",
    "OrderItemCreate",
    "OrderItemResponse",
    "OrderBase",
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderListResponse",
    # Review
    "ReviewBase",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "ReviewWithUser",
    # Rewards
    "RewardsBase",
    "RewardsCreate",
    "RewardsUpdate",
    "RewardsResponse",
    "RewardsTransaction",
    # Payment
    "PaymentMethod",
    "PaymentStatus",
    "PaymentBase",
    "PaymentCreate",
    "PaymentUpdate",
    "PaymentResponse",
]