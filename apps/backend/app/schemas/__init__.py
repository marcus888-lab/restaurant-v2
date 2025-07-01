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
    CoffeeWithCategory,
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CoffeeCreateRequest,
    CoffeeUpdateRequest
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
    OrderListResponse,
    OrderDetailResponse,
    OrderItemDetailResponse,
    OrderCreateRequest,
    OrderItemRequest,
    OrderUpdateStatus
)
from .review import (
    ReviewBase,
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewWithUser,
    ReviewCreateRequest,
    ReviewUpdateRequest
)
from .rewards import (
    RewardsBase,
    RewardsCreate,
    RewardsUpdate,
    RewardsResponse,
    RewardsTransaction,
    RewardsRedeemRequest,
    RewardsHistoryResponse
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
    "CategoryCreateRequest",
    "CategoryUpdateRequest",
    "CoffeeCreateRequest",
    "CoffeeUpdateRequest",
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
    "OrderDetailResponse",
    "OrderItemDetailResponse",
    "OrderCreateRequest",
    "OrderItemRequest",
    "OrderUpdateStatus",
    # Review
    "ReviewBase",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "ReviewWithUser",
    "ReviewCreateRequest",
    "ReviewUpdateRequest",
    # Rewards
    "RewardsBase",
    "RewardsCreate",
    "RewardsUpdate",
    "RewardsResponse",
    "RewardsTransaction",
    "RewardsRedeemRequest",
    "RewardsHistoryResponse",
    # Payment
    "PaymentMethod",
    "PaymentStatus",
    "PaymentBase",
    "PaymentCreate",
    "PaymentUpdate",
    "PaymentResponse",
]