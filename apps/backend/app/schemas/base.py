"""
Base schemas and common response models.
"""
from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


# Generic type for response data
DataT = TypeVar("DataT")


class StandardResponse(BaseModel, Generic[DataT]):
    """Standard API response format."""
    success: bool = True
    data: Optional[DataT] = None
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    """Error response format."""
    success: bool = False
    error: dict[str, Any] = Field(
        ...,
        example={
            "code": "INVALID_REQUEST",
            "message": "请求参数错误",
            "details": "Coffee ID not found"
        }
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Paginated response format."""
    success: bool = True
    data: List[DataT] = []
    pagination: dict[str, Any] = Field(
        ...,
        example={
            "page": 1,
            "limit": 20,
            "total": 100,
            "hasNext": True
        }
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))