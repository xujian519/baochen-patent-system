"""
案件管理 API 路由
提供案件的 CRUD 接口，包含编号自动生成、状态变更时间线记录
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_active_user
from app.models.user import User
from app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseBrief,
    CaseDetail,
    CaseListResponse,
    CaseStatusUpdate,
)
from app.schemas.common import APIResponse
from app.services.case import CaseService


router = APIRouter(prefix="/cases", tags=["案件管理"])


@router.get("/", response_model=APIResponse[CaseListResponse], summary="获取案件列表")
async def get_cases(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词（案件名/案件编号/客户名）"),
    stage: Optional[str] = Query(None, description="案件阶段筛选"),
    case_status: Optional[str] = Query(None, description="案件状态筛选"),
    patent_type: Optional[str] = Query(None, description="专利类型筛选"),
    client_id: Optional[int] = Query(None, description="客户ID筛选"),
    agent_id: Optional[int] = Query(None, description="代理师ID筛选"),
    entity: Optional[str] = Query(None, description="主体筛选（宝宸/瑞宸）"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取案件列表（分页、搜索、筛选）

    - **page**: 页码，从1开始
    - **page_size**: 每页数量，默认20，最大100
    - **search**: 搜索关键词（案件名、案件编号、申请号、客户名）
    - **stage**: 案件阶段筛选（新案/撰写中/待质检/已定稿/待递交/已递交-在审/答复OA/授权/驳回/放弃/结案归档）
    - **case_status**: 案件状态筛选（进行中/已结案/已终止/已暂停）
    - **patent_type**: 专利类型筛选（发明/实用新型/外观设计）
    - **client_id**: 按客户筛选
    - **agent_id**: 按代理师筛选
    - **entity**: 按主体筛选（宝宸/瑞宸）
    """
    skip = (page - 1) * page_size
    cases, total = await CaseService.get_cases(
        db,
        skip=skip,
        limit=page_size,
        search=search,
        stage=stage,
        case_status=case_status,
        patent_type=patent_type,
        client_id=client_id,
        agent_id=agent_id,
        entity=entity,
    )

    return APIResponse(
        data=CaseListResponse(
            items=[CaseBrief.model_validate(c) for c in cases],
            total=total,
            page=page,
            page_size=page_size
        )
    )


@router.get("/search", response_model=APIResponse[CaseListResponse], summary="案件搜索")
async def search_cases(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    全文搜索案件

    搜索范围：案件名、案件编号、申请号、申请人、发明人
    """
    skip = (page - 1) * page_size
    cases, total = await CaseService.search_cases(db, keyword, skip=skip, limit=page_size)

    return APIResponse(
        data=CaseListResponse(
            items=[CaseBrief.model_validate(c) for c in cases],
            total=total,
            page=page,
            page_size=page_size
        )
    )


@router.get("/statistics", response_model=APIResponse[dict], summary="案件统计")
async def get_case_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取案件统计信息

    返回按状态和专利类型的案件数量统计
    """
    stats = await CaseService.get_case_statistics(db)
    return APIResponse(data=stats)


@router.get("/{case_id}", response_model=APIResponse[CaseDetail], summary="获取案件详情")
async def get_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取案件详情（含关联数据）

    返回案件基本信息及关联的客户、费用、文档、期限、时间线等
    """
    case = await CaseService.get_case_detail(db, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案件ID {case_id} 不存在"
        )

    return APIResponse(data=CaseDetail.model_validate(case))


@router.get(
    "/number/{case_number}",
    response_model=APIResponse[CaseResponse],
    summary="根据编号获取案件"
)
async def get_case_by_number(
    case_number: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    根据案件编号获取案件

    - **case_number**: 案件编号（如 BCZL2026031001）
    """
    case = await CaseService.get_case_by_number(db, case_number)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案件编号 {case_number} 不存在"
        )

    return APIResponse(data=CaseResponse.model_validate(case))


@router.post(
    "/",
    response_model=APIResponse[CaseResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建案件"
)
async def create_case(
    case_data: CaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新案件（自动生成案件编号）

    案件编号格式：BCZL + 年月(6位) + 类型(1位) + 流水号(3位)
    示例：BCZL2026031001

    - **client_id**: 客户ID（必填）
    - **title**: 发明名称（必填）
    - **patent_type**: 专利类型（必填：发明/实用新型/外观设计）
    - 其他字段可选
    """
    try:
        case = await CaseService.create_case(db, case_data)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    return APIResponse(
        code=201,
        message=f"案件创建成功，编号：{case.case_number}",
        data=CaseResponse.model_validate(case)
    )


@router.put("/{case_id}", response_model=APIResponse[CaseResponse], summary="更新案件")
async def update_case(
    case_id: int,
    case_data: CaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新案件信息

    所有字段均为可选，只更新提供的字段
    """
    case = await CaseService.update_case(db, case_id, case_data)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案件ID {case_id} 不存在"
        )

    return APIResponse(
        message="案件更新成功",
        data=CaseResponse.model_validate(case)
    )


@router.patch("/{case_id}/status", response_model=APIResponse[CaseResponse], summary="更新案件状态")
async def update_case_status(
    case_id: int,
    status_data: CaseStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新案件状态（自动记录时间线）

    - **status**: 新状态
    - **notes**: 备注说明（可选）

    状态变更会自动记录到案件时间线中
    """
    case = await CaseService.update_case_status(db, case_id, status_data)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案件ID {case_id} 不存在"
        )

    return APIResponse(
        message=f"案件状态已更新为 '{case.status}'",
        data=CaseResponse.model_validate(case)
    )


@router.delete("/{case_id}", response_model=APIResponse, summary="删除案件")
async def delete_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除案件

    注意：删除案件会级联删除关联的费用、文档、期限、来文、时间线等数据
    """
    # 先检查是否存在
    case = await CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案件ID {case_id} 不存在"
        )

    success = await CaseService.delete_case(db, case_id)
    if success:
        return APIResponse(message="案件删除成功")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除案件失败"
        )
