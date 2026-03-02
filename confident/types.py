from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic

# Type variable for the 'data' field in ApiResponse
T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard envelope for all Confident AI responses."""

    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    deprecated: Optional[bool] = False
    link: Optional[str] = None  # Link to documentation or dashboard for errors


class ConfidentApiError(Exception):
    """Custom exception that preserves API response metadata."""

    def __init__(self, message: str, status_code: int, link: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.link = link
