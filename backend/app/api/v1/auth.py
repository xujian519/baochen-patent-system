"""
认证 API 路由
提供用户注册、登录、获取当前用户信息等接口
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    LoginResponse,
)
from app.services.auth import AuthService
from app.middleware.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    description="创建新用户账号"
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册

    - **name**: 用户姓名
    - **email**: 邮箱地址(唯一)
    - **password**: 密码(6-100位)
    - **role**: 角色(admin/agent/staff)
    - **entity**: 主体(宝宸/瑞宸)
    - **phone**: 电话(可选)
    - **agent_number**: 代理师资格证号(可选)
    """
    user = await AuthService.register_user(db, user_data)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="用户登录",
    description="使用邮箱和密码登录,返回 JWT 令牌"
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    - **email**: 邮箱地址
    - **password**: 密码

    返回:
    - **access_token**: JWT 访问令牌
    - **token_type**: 令牌类型(bearer)
    - **user**: 用户信息
    """
    # 验证用户凭据
    user = await AuthService.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not user:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token = AuthService.create_user_token(user.id)

    # 返回登录响应
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="获取当前用户信息",
    description="获取当前认证用户的详细信息"
)
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户信息

    需要在请求头中携带有效的 JWT 令牌:
    ```
    Authorization: Bearer <token>
    ```
    """
    return UserResponse.model_validate(current_user)
