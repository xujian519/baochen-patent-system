"""
客户管理 API 路由
提供客户的 CRUD 接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_active_user
from app.models.user import User
from app.schemas.client import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientWithCases,
    ClientListResponse,
)
from app.schemas.common import APIResponse
from app.services.client import ClientService


router = APIRouter(prefix="/clients", tags=["客户管理"])


@router.get("/", response_model=APIResponse[ClientListResponse], summary="获取客户列表")
async def get_clients(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    client_type: Optional[str] = Query(None, description="客户类型筛选"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取客户列表（分页）

    - **page**: 页码，从1开始
    - **page_size**: 每页数量，默认20，最大100
    - **search**: 搜索关键词（客户名、简称、联系人、电话）
    - **client_type**: 客户类型筛选（企业/个人）
    """
    skip = (page - 1) * page_size
    clients, total = await ClientService.get_clients(
        db, skip=skip, limit=page_size, search=search, client_type=client_type
    )

    return APIResponse(
        data=ClientListResponse(
            items=[ClientResponse.model_validate(c) for c in clients],
            total=total,
            page=page,
            page_size=page_size
        )
    )


@router.get("/{client_id}", response_model=APIResponse[ClientWithCases], summary="获取客户详情")
async def get_client(
    client_id: int,
    include_cases: bool = Query(False, description="是否包含关联案件"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取客户详情

    - **client_id**: 客户ID
    - **include_cases**: 是否包含关联的案件列表
    """
    if include_cases:
        client = await ClientService.get_client_with_cases(db, client_id)
    else:
        client = await ClientService.get_client(db, client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"客户ID {client_id} 不存在"
        )

    # 根据是否包含案件返回不同的模型
    if include_cases:
        return APIResponse(data=ClientWithCases.model_validate(client))
    else:
        # 不包含案件时，也使用 ClientWithCases 模型，但 cases 为空列表
        return APIResponse(data=ClientWithCases.model_validate(client))


@router.post(
    "/",
    response_model=APIResponse[ClientResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建客户"
)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新客户

    - **name**: 客户名称（必填）
    - **short_name**: 客户简称
    - **contact_person**: 联系人
    - **phone**: 电话
    - **email**: 邮箱
    - **address**: 地址
    - **type**: 类型（企业/个人）
    - **credit_code**: 统一社会信用代码
    - **fee_reduction**: 是否费减
    - **notes**: 备注
    """
    client = await ClientService.create_client(db, client_data)
    return APIResponse(
        code=201,
        message="客户创建成功",
        data=ClientResponse.model_validate(client)
    )


@router.put("/{client_id}", response_model=APIResponse[ClientResponse], summary="更新客户")
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新客户信息

    所有字段均为可选，只更新提供的字段
    """
    client = await ClientService.update_client(db, client_id, client_data)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"客户ID {client_id} 不存在"
        )

    return APIResponse(
        message="客户更新成功",
        data=ClientResponse.model_validate(client)
    )


@router.delete("/{client_id}", response_model=APIResponse, summary="删除客户")
async def delete_client(
    client_id: int,
    force: bool = Query(False, description="强制删除（即使有关联案件）"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除客户

    - **force**: 是否强制删除（即使有关联案件）

    注意：如果客户有关联案件且未设置 force=True，将无法删除
    """
    # 检查客户是否存在
    client = await ClientService.get_client(db, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"客户ID {client_id} 不存在"
        )

    # 检查是否有关联案件
    has_cases = await ClientService.check_client_has_cases(db, client_id)
    if has_cases and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该客户有关联的案件，无法删除。如需删除请设置 force=True"
        )

    # 执行删除
    success = await ClientService.delete_client(db, client_id)
    if success:
        return APIResponse(message="客户删除成功")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除客户失败"
        )
