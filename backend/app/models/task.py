"""
任务模型
管理代理师和员工的工作任务
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Task(Base):
    """任务表"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    title = Column(String(500), nullable=False, comment="任务标题")
    description = Column(Text, comment="任务描述")

    # 关联客户(可选)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, comment="客户ID")
    client_name = Column(String(200), comment="客户名称(冗余)")
    client_short_name = Column(String(100), comment="客户简称(冗余)")

    # 关联案件(可选)
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")
    case_number = Column(String(50), comment="案件编号(冗余)")
    application_number = Column(String(50), comment="申请号(冗余)")

    # 任务信息
    task_type = Column(String(50), nullable=False, comment="任务类型: 撰写/答复OA/客户沟通/内部事务/质检/归档/其他")
    priority = Column(String(20), default="中", comment="优先级: 紧急/高/中/低")
    status = Column(String(20), default="待开始", comment="状态: 待开始/进行中/待审核/已完成/已取消")

    # 人员分配
    assignee_id = Column(Integer, ForeignKey("users.id"), comment="负责人ID")
    assistant_id = Column(Integer, ForeignKey("users.id"), comment="协助人ID")

    # 时间信息
    start_date = Column(Date, comment="开始日期")
    due_date = Column(Date, comment="截止日期")
    completed_date = Column(Date, comment="完成日期")

    # 进度
    progress = Column(Integer, default=0, comment="进度(0-100)")

    # 备注
    notes = Column(Text, comment="备注")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    client = relationship("Client", back_populates="tasks")
    case = relationship("Case", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_as_assignee", foreign_keys=[assignee_id])
    assistant = relationship("User", back_populates="tasks_as_assistant", foreign_keys=[assistant_id])

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title[:20]}..., status={self.status})>"
