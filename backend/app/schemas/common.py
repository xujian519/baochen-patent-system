"""
通用 Schemas
用于分页和通用响应
"""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """通用分页响应模型"""
    items: List[T]
    total: int
    page: int
    page_size: int

    class Config:
        from_attributes = True


class APIResponse(BaseModel, Generic[T]):
    """API 标准响应格式"""
    code: int = 200
    data: Optional[T] = None
    message: str = "ok"

    class Config:
        from_attributes = True
