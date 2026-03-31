"""
Pydantic Schemas 包
用于 API 请求和响应的数据验证
"""
from app.schemas.client import (
    ClientBase,
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientWithCases,
    ClientListResponse
)
from app.schemas.case import (
    CaseBase,
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseBrief,
    CaseDetail,
    CaseListResponse
)
from app.schemas.common import PaginatedResponse
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenData,
    LoginResponse,
)

__all__ = [
    # Client schemas
    "ClientBase",
    "ClientCreate",
    "ClientUpdate",
    "ClientResponse",
    "ClientWithCases",
    "ClientListResponse",
    # Case schemas
    "CaseBase",
    "CaseCreate",
    "CaseUpdate",
    "CaseResponse",
    "CaseBrief",
    "CaseDetail",
    "CaseListResponse",
    # Common schemas
    "PaginatedResponse",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    "LoginResponse",
]
