"""
期限模型
管理案件的各种期限，支持3级预警
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Deadline(Base):
    """期限表"""
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")

    # 期限信息
    deadline_type = Column(String(50), nullable=False, comment="期限类型: OA答复/年费/递交/其他")
    deadline_date = Column(Date, nullable=False, index=True, comment="截止日期")
    warning_level = Column(Integer, default=0, comment="预警级别: 0-3 (0=无, 1=15天, 2=7天, 3=3天)")
    description = Column(Text, comment="描述")

    # 完成状态
    is_completed = Column(Boolean, default=False, comment="是否已完成")
    completed_date = Column(Date, comment="完成日期")
    reminded_at = Column(DateTime, comment="最近提醒时间")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="deadlines")

    def __repr__(self):
        return f"<Deadline(id={self.id}, case_id={self.case_id}, deadline_type={self.deadline_type}, deadline_date={self.deadline_date})>"
