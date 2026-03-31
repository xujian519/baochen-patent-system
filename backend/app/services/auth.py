"""
认证服务模块
提供用户注册、登录、令牌验证等功能
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import verify_password, get_password_hash
from app.utils.jwt_handler import create_access_token, decode_access_token


class AuthService:
    """认证服务类"""

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        注册新用户

        Args:
            db: 数据库会话
            user_data: 用户注册数据

        Returns:
            User: 创建的用户对象

        Raises:
            HTTPException: 邮箱已被注册时抛出 400 错误
        """
        # 检查邮箱是否已存在
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )

        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            entity=user_data.entity,
            phone=user_data.phone,
            agent_number=user_data.agent_number,
            password_hash=hashed_password,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db.add(new_user)
        await db.flush()  # 刷新以获取 ID
        await db.refresh(new_user)  # 刷新以获取完整数据

        return new_user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        验证用户凭据

        Args:
            db: 数据库会话
            email: 用户邮箱
            password: 明文密码

        Returns:
            Optional[User]: 验证成功返回用户对象,失败返回 None
        """
        # 查找用户
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # 用户不存在或密码不匹配
        if not user or not verify_password(password, user.password_hash):
            return None

        # 用户已被禁用
        if not user.is_active:
            return None

        return user

    @staticmethod
    async def get_current_user(db: AsyncSession, token: str) -> User:
        """
        从 JWT 令牌获取当前用户

        Args:
            db: 数据库会话
            token: JWT 令牌

        Returns:
            User: 当前用户对象

        Raises:
            HTTPException: 令牌无效或用户不存在时抛出 401 错误
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # 解码令牌
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        # 获取用户 ID
        user_id: Optional[int] = payload.get("sub")
        if user_id is not None:
            user_id = int(user_id)
        if user_id is None:
            raise credentials_exception

        # 查询用户
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        # 检查用户是否激活
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户已被禁用"
            )

        return user

    @staticmethod
    def create_user_token(user_id: int) -> str:
        """
        为用户创建访问令牌

        Args:
            user_id: 用户 ID

        Returns:
            str: JWT 访问令牌
        """
        # 令牌载荷中存储用户 ID
        token_data = {"sub": user_id}
        access_token = create_access_token(token_data)
        return access_token
