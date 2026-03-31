"""
认证中间件和依赖
提供 FastAPI Depends 可用的认证依赖函数
"""
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.auth import AuthService

# HTTP Bearer 令牌认证方案
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前认证用户的依赖

    Args:
        credentials: HTTP Bearer 凭据
        db: 数据库会话

    Returns:
        User: 当前认证的用户

    Raises:
        HTTPException: 认证失败时抛出 401 错误
    """
    token = credentials.credentials
    user = await AuthService.get_current_user(db, token)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户的依赖

    Args:
        current_user: 当前用户

    Returns:
        User: 当前活跃用户

    Raises:
        HTTPException: 用户未激活时抛出 403 错误
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账号已被禁用"
        )
    return current_user


def require_role(allowed_roles: List[str]):
    """
    角色权限检查依赖工厂

    Args:
        allowed_roles: 允许访问的角色列表

    Returns:
        依赖函数
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """
        检查用户角色是否在允许列表中

        Args:
            current_user: 当前用户

        Returns:
            User: 当前用户

        Raises:
            HTTPException: 权限不足时抛出 403 错误
        """
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足,需要以下角色之一: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker


# 常用角色依赖
require_admin = require_role(["admin"])
require_agent = require_role(["admin", "agent"])
require_staff = require_role(["admin", "agent", "staff"])
