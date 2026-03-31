"""
用户管理 API 路由
提供用户列表接口（用于下拉选择）
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.middleware.auth import get_current_active_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse


router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/", response_model=APIResponse[List[UserResponse]], summary="获取用户列表")
async def get_users(
    role: Optional[str] = Query(None, description="角色筛选 (admin/agent/staff)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户列表（用于下拉选择）

    - **role**: 按角色筛选 (admin/agent/staff)
    """
    stmt = select(User).where(User.is_active == True)

    if role:
        stmt = stmt.where(User.role == role)

    stmt = stmt.order_by(User.name)
    result = await db.execute(stmt)
    users = list(result.scalars().all())

    return APIResponse(data=[UserResponse.model_validate(u) for u in users])
