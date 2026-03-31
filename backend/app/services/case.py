"""
案件服务层
处理案件相关的业务逻辑
"""
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from sqlalchemy import select, or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.case import Case
from app.models.client import Client
from app.models.user import User
from app.models.timeline import CaseTimeline
from app.schemas.case import CaseCreate, CaseUpdate, CaseStatusUpdate
from app.services.numbering import NumberingService
from app.utils.security import get_password_hash


class CaseService:
    """案件服务类"""

    @staticmethod
    async def _get_or_create_client(db: AsyncSession, client_id: Optional[int], client_name: Optional[str]) -> Optional[int]:
        """
        获取或创建客户

        Args:
            db: 数据库会话
            client_id: 客户ID（优先使用）
            client_name: 客户名称（用于查找或创建）

        Returns:
            客户ID
        """
        # 优先使用 client_id
        if client_id:
            return client_id

        # 如果没有 client_name，返回 None
        if not client_name or not client_name.strip():
            return None

        client_name = client_name.strip()

        # 尝试查找现有客户（按名称或简称匹配）
        stmt = select(Client).where(
            or_(Client.name == client_name, Client.short_name == client_name)
        )
        result = await db.execute(stmt)
        existing_client = result.scalar_one_or_none()

        if existing_client:
            return existing_client.id

        # 创建新客户
        new_client = Client(
            name=client_name,
            type="企业",  # 默认类型
        )
        db.add(new_client)
        await db.flush()
        return new_client.id

    @staticmethod
    async def _get_or_create_user(db: AsyncSession, user_id: Optional[int], user_name: Optional[str], role: str) -> Optional[int]:
        """
        获取或创建用户（代理师或员工）

        Args:
            db: 数据库会话
            user_id: 用户ID（优先使用）
            user_name: 用户名称（用于查找或创建）
            role: 用户角色 (agent/staff)

        Returns:
            用户ID
        """
        # 优先使用 user_id
        if user_id:
            return user_id

        # 如果没有 user_name，返回 None
        if not user_name or not user_name.strip():
            return None

        user_name = user_name.strip()

        # 尝试查找现有用户（按姓名匹配）
        stmt = select(User).where(User.name == user_name, User.role == role)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return existing_user.id

        # 创建新用户
        new_user = User(
            name=user_name,
            email=f"{user_name}@baochen.com",  # 生成默认邮箱
            role=role,
            entity="宝宸",
            password_hash=get_password_hash("123456"),  # 设置默认密码
        )
        db.add(new_user)
        await db.flush()
        return new_user.id

    @staticmethod
    async def create_case(db: AsyncSession, case_data: CaseCreate) -> Case:
        """
        创建案件（自动生成案件编号）

        Args:
            db: 数据库会话
            case_data: 案件创建数据

        Returns:
            创建的案件对象
        """
        # 处理客户ID（支持自定义输入）
        client_id = await CaseService._get_or_create_client(
            db, case_data.client_id, case_data.client_name
        )

        # 处理代理师ID（支持自定义输入）
        agent_id = await CaseService._get_or_create_user(
            db, case_data.agent_id, case_data.agent_name, "agent"
        )

        # 处理协办人ID（支持自定义输入）
        assistant_id = await CaseService._get_or_create_user(
            db, case_data.assistant_id, case_data.assistant_name, "staff"
        )

        # 生成案件编号
        case_number = await NumberingService.generate_case_number_with_retry(
            db, case_data.patent_type
        )

        # 构建案件数据（排除自定义名称字段）
        case_dict = case_data.model_dump(exclude={"client_name", "agent_name", "assistant_name"})
        case_dict["case_number"] = case_number
        case_dict["client_id"] = client_id
        case_dict["agent_id"] = agent_id
        case_dict["assistant_id"] = assistant_id

        case = Case(**case_dict)
        db.add(case)
        await db.flush()

        # 创建初始时间线记录
        timeline = CaseTimeline(
            case_id=case.id,
            status=case.stage,
            event_type="创建案件",
            event_date=date.today(),
            description=f"创建案件，编号：{case_number}",
        )
        db.add(timeline)

        await db.flush()
        await db.refresh(case)
        return case

    @staticmethod
    async def get_case(db: AsyncSession, case_id: int) -> Optional[Case]:
        """
        获取单个案件

        Args:
            db: 数据库会话
            case_id: 案件ID

        Returns:
            案件对象，不存在则返回None
        """
        stmt = select(Case).where(Case.id == case_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_case_detail(db: AsyncSession, case_id: int) -> Optional[Case]:
        """
        获取案件详情（含关联数据）

        Args:
            db: 数据库会话
            case_id: 案件ID

        Returns:
            案件对象（含关联数据），不存在则返回None
        """
        stmt = (
            select(Case)
            .options(
                selectinload(Case.client),
                selectinload(Case.fees),
                selectinload(Case.documents),
                selectinload(Case.deadlines),
                selectinload(Case.timelines),
            )
            .where(Case.id == case_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_case_by_number(db: AsyncSession, case_number: str) -> Optional[Case]:
        """
        根据案件编号获取案件

        Args:
            db: 数据库会话
            case_number: 案件编号

        Returns:
            案件对象，不存在则返回None
        """
        stmt = select(Case).where(Case.case_number == case_number)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_cases(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        stage: Optional[str] = None,
        case_status: Optional[str] = None,
        patent_type: Optional[str] = None,
        client_id: Optional[int] = None,
        agent_id: Optional[int] = None,
        entity: Optional[str] = None,
    ) -> tuple[List[Case], int]:
        """
        获取案件列表（分页、搜索、筛选）

        Args:
            db: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            search: 搜索关键词（案件名、案件编号、客户名）
            stage: 案件阶段筛选
            case_status: 案件状态筛选
            patent_type: 专利类型筛选
            client_id: 客户ID筛选
            agent_id: 代理师ID筛选
            entity: 主体筛选

        Returns:
            (案件列表, 总数)
        """
        # 构建基础查询（关联客户表用于搜索，加载 agent 和 assistant）
        stmt = select(Case).options(
            selectinload(Case.client),
            selectinload(Case.agent),
            selectinload(Case.assistant),
        )
        count_stmt = select(func.count(Case.id))

        # 搜索条件
        if search:
            search_pattern = f"%{search}%"
            search_condition = or_(
                Case.title.ilike(search_pattern),
                Case.case_number.ilike(search_pattern),
                Case.application_number.ilike(search_pattern),
                Client.name.ilike(search_pattern),
            )
            stmt = stmt.join(Client, isouter=True).where(search_condition)
            count_stmt = count_stmt.join(Client, isouter=True).where(search_condition)

        # 案件阶段筛选
        if stage:
            stmt = stmt.where(Case.stage == stage)
            count_stmt = count_stmt.where(Case.stage == stage)

        # 案件状态筛选
        if case_status:
            stmt = stmt.where(Case.case_status == case_status)
            count_stmt = count_stmt.where(Case.case_status == case_status)

        # 专利类型筛选
        if patent_type:
            stmt = stmt.where(Case.patent_type == patent_type)
            count_stmt = count_stmt.where(Case.patent_type == patent_type)

        # 客户筛选
        if client_id:
            stmt = stmt.where(Case.client_id == client_id)
            count_stmt = count_stmt.where(Case.client_id == client_id)

        # 代理师筛选
        if agent_id:
            stmt = stmt.where(Case.agent_id == agent_id)
            count_stmt = count_stmt.where(Case.agent_id == agent_id)

        # 主体筛选
        if entity:
            stmt = stmt.where(Case.entity == entity)
            count_stmt = count_stmt.where(Case.entity == entity)

        # 获取总数
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # 分页查询（按创建时间倒序）
        stmt = stmt.order_by(Case.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        cases = list(result.scalars().unique().all())

        return cases, total

    @staticmethod
    async def update_case(
        db: AsyncSession,
        case_id: int,
        case_data: CaseUpdate
    ) -> Optional[Case]:
        """
        更新案件

        Args:
            db: 数据库会话
            case_id: 案件ID
            case_data: 案件更新数据

        Returns:
            更新后的案件对象，不存在则返回None
        """
        case = await CaseService.get_case(db, case_id)
        if not case:
            return None

        # 处理客户ID（支持自定义输入）
        if case_data.client_id is not None or case_data.client_name is not None:
            client_id = await CaseService._get_or_create_client(
                db, case_data.client_id, case_data.client_name
            )
            case.client_id = client_id

        # 处理代理师ID（支持自定义输入）
        if case_data.agent_id is not None or case_data.agent_name is not None:
            agent_id = await CaseService._get_or_create_user(
                db, case_data.agent_id, case_data.agent_name, "agent"
            )
            case.agent_id = agent_id

        # 处理协办人ID（支持自定义输入）
        if case_data.assistant_id is not None or case_data.assistant_name is not None:
            assistant_id = await CaseService._get_or_create_user(
                db, case_data.assistant_id, case_data.assistant_name, "staff"
            )
            case.assistant_id = assistant_id

        # 更新其他字段（排除 ID 和名称字段）
        update_data = case_data.model_dump(
            exclude_unset=True,
            exclude={"client_id", "client_name", "agent_id", "agent_name", "assistant_id", "assistant_name"}
        )
        for field, value in update_data.items():
            setattr(case, field, value)

        await db.flush()
        await db.refresh(case)
        return case

    @staticmethod
    async def update_case_status(
        db: AsyncSession,
        case_id: int,
        status_data: CaseStatusUpdate,
        operator: Optional[str] = None
    ) -> Optional[Case]:
        """
        更新案件状态（自动记录时间线）

        Args:
            db: 数据库会话
            case_id: 案件ID
            status_data: 状态更新数据
            operator: 操作人

        Returns:
            更新后的案件对象，不存在则返回None
        """
        case = await CaseService.get_case(db, case_id)
        if not case:
            return None

        timeline_events = []

        # 更新案件阶段
        if status_data.stage:
            old_stage = case.stage
            new_stage = status_data.stage
            case.stage = new_stage
            timeline_events.append(f"阶段从 '{old_stage}' 变更为 '{new_stage}'")

        # 更新案件状态
        if status_data.case_status:
            old_status = case.case_status
            new_status = status_data.case_status
            case.case_status = new_status
            timeline_events.append(f"状态从 '{old_status}' 变更为 '{new_status}'")

        # 创建时间线记录
        if timeline_events:
            description = "、".join(timeline_events)
            if status_data.notes:
                description += f"，备注：{status_data.notes}"

            timeline = CaseTimeline(
                case_id=case.id,
                status=case.stage,
                event_type="状态变更",
                event_date=date.today(),
                description=description,
                operator=operator,
            )
            db.add(timeline)

        await db.flush()
        await db.refresh(case)
        return case

    @staticmethod
    async def search_cases(
        db: AsyncSession,
        keyword: str,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Case], int]:
        """
        案件搜索（全文搜索）

        Args:
            db: 数据库会话
            keyword: 搜索关键词
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            (案件列表, 总数)
        """
        search_pattern = f"%{keyword}%"

        # 构建搜索条件
        search_condition = or_(
            Case.title.ilike(search_pattern),
            Case.case_number.ilike(search_pattern),
            Case.application_number.ilike(search_pattern),
            Case.applicant.ilike(search_pattern),
            Case.inventor.ilike(search_pattern),
        )

        # 计数查询
        count_stmt = select(func.count(Case.id)).where(search_condition)
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # 分页查询
        stmt = (
            select(Case)
            .where(search_condition)
            .order_by(Case.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        cases = list(result.scalars().all())

        return cases, total

    @staticmethod
    async def delete_case(db: AsyncSession, case_id: int) -> bool:
        """
        删除案件（注意：会级联删除关联数据）

        Args:
            db: 数据库会话
            case_id: 案件ID

        Returns:
            删除成功返回True，案件不存在返回False
        """
        case = await CaseService.get_case(db, case_id)
        if not case:
            return False

        await db.delete(case)
        await db.flush()
        return True

    @staticmethod
    async def get_case_statistics(db: AsyncSession) -> dict:
        """
        获取案件统计信息

        Args:
            db: 数据库会话

        Returns:
            统计信息字典
        """
        # 按案件阶段统计
        stage_stmt = (
            select(Case.stage, func.count(Case.id))
            .group_by(Case.stage)
        )
        stage_result = await db.execute(stage_stmt)
        stage_stats = dict(stage_result.all())

        # 按案件状态统计
        status_stmt = (
            select(Case.case_status, func.count(Case.id))
            .group_by(Case.case_status)
        )
        status_result = await db.execute(status_stmt)
        status_stats = dict(status_result.all())

        # 按专利类型统计
        type_stmt = (
            select(Case.patent_type, func.count(Case.id))
            .group_by(Case.patent_type)
        )
        type_result = await db.execute(type_stmt)
        type_stats = dict(type_result.all())

        # 总数
        total_stmt = select(func.count(Case.id))
        total_result = await db.execute(total_stmt)
        total = total_result.scalar_one()

        return {
            "total": total,
            "by_stage": stage_stats,
            "by_status": status_stats,
            "by_patent_type": type_stats,
        }
