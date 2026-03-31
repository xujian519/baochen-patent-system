"""
客户服务层
处理客户相关的业务逻辑
"""
from typing import List, Optional
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.client import Client
from app.models.case import Case
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    """客户服务类"""

    @staticmethod
    async def create_client(db: AsyncSession, client_data: ClientCreate) -> Client:
        """
        创建客户

        Args:
            db: 数据库会话
            client_data: 客户创建数据

        Returns:
            创建的客户对象
        """
        client = Client(**client_data.model_dump())
        db.add(client)
        await db.flush()  # 获取生成的ID
        await db.refresh(client)
        return client

    @staticmethod
    async def get_client(db: AsyncSession, client_id: int) -> Optional[Client]:
        """
        获取单个客户

        Args:
            db: 数据库会话
            client_id: 客户ID

        Returns:
            客户对象，不存在则返回None
        """
        stmt = select(Client).where(Client.id == client_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_client_with_cases(db: AsyncSession, client_id: int) -> Optional[Client]:
        """
        获取客户及其关联的案件

        Args:
            db: 数据库会话
            client_id: 客户ID

        Returns:
            客户对象（含关联案件），不存在则返回None
        """
        stmt = (
            select(Client)
            .options(selectinload(Client.cases))
            .where(Client.id == client_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_clients(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        client_type: Optional[str] = None
    ) -> tuple[List[Client], int]:
        """
        获取客户列表（分页、搜索）

        Args:
            db: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            search: 搜索关键词（客户名、联系人、电话）
            client_type: 客户类型筛选

        Returns:
            (客户列表, 总数)
        """
        # 构建基础查询
        stmt = select(Client)

        # 构建计数查询
        count_stmt = select(func.count(Client.id))

        # 搜索条件
        if search:
            search_pattern = f"%{search}%"
            search_condition = or_(
                Client.name.ilike(search_pattern),
                Client.short_name.ilike(search_pattern),
                Client.contact_person.ilike(search_pattern),
                Client.phone.ilike(search_pattern),
            )
            stmt = stmt.where(search_condition)
            count_stmt = count_stmt.where(search_condition)

        # 类型筛选
        if client_type:
            stmt = stmt.where(Client.type == client_type)
            count_stmt = count_stmt.where(Client.type == client_type)

        # 获取总数
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # 分页查询
        stmt = stmt.order_by(Client.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        clients = list(result.scalars().all())

        return clients, total

    @staticmethod
    async def update_client(
        db: AsyncSession,
        client_id: int,
        client_data: ClientUpdate
    ) -> Optional[Client]:
        """
        更新客户

        Args:
            db: 数据库会话
            client_id: 客户ID
            client_data: 客户更新数据

        Returns:
            更新后的客户对象，不存在则返回None
        """
        client = await ClientService.get_client(db, client_id)
        if not client:
            return None

        # 只更新提供的字段
        update_data = client_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        await db.flush()
        await db.refresh(client)
        return client

    @staticmethod
    async def delete_client(db: AsyncSession, client_id: int) -> bool:
        """
        删除客户

        注意：如果客户有关联的案件，会因外键约束而删除失败

        Args:
            db: 数据库会话
            client_id: 客户ID

        Returns:
            删除成功返回True，客户不存在返回False
        """
        client = await ClientService.get_client(db, client_id)
        if not client:
            return False

        await db.delete(client)
        await db.flush()
        return True

    @staticmethod
    async def check_client_has_cases(db: AsyncSession, client_id: int) -> bool:
        """
        检查客户是否有关联案件

        Args:
            db: 数据库会话
            client_id: 客户ID

        Returns:
            有案件返回True，否则返回False
        """
        stmt = select(func.count(Case.id)).where(Case.client_id == client_id)
        result = await db.execute(stmt)
        count = result.scalar_one()
        return count > 0
