"""
API v1 模块
"""
from app.api.v1.auth import router as auth_router
from app.api.v1.clients import router as clients_router
from app.api.v1.cases import router as cases_router
from app.api.v1.users import router as users_router

__all__ = ["auth_router", "clients_router", "cases_router", "users_router"]
