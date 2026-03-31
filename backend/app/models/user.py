"""
用户模型
系统用户表，包含管理员、代理师、员工等角色
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="姓名")
    role = Column(String(50), default="staff", comment="角色: admin/agent/staff")
    entity = Column(String(20), default="宝宸", comment="主体: 宝宸/瑞宸")
    agent_number = Column(String(50), comment="代理师资格证号")
    email = Column(String(200), unique=True, index=True, comment="邮箱")
    phone = Column(String(50), comment="电话")
    password_hash = Column(String(200), nullable=False, comment="密码哈希")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    cases_as_agent = relationship("Case", back_populates="agent", foreign_keys="Case.agent_id")
    cases_as_assistant = relationship("Case", back_populates="assistant", foreign_keys="Case.assistant_id")
    tasks_as_assignee = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    tasks_as_assistant = relationship("Task", back_populates="assistant", foreign_keys="Task.assistant_id")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, role={self.role})>"
