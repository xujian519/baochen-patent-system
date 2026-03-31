"""
案件时间线模型
记录案件的状态变更和历史事件
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class CaseTimeline(Base):
    """案件时间线表"""
    __tablename__ = "case_timeline"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")

    # 事件信息
    status = Column(String(50), nullable=False, comment="状态")
    event_type = Column(String(50), nullable=False, comment="事件类型")
    event_date = Column(Date, nullable=False, comment="事件日期")
    description = Column(Text, comment="描述")
    operator = Column(String(100), comment="操作人")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="timelines")

    def __repr__(self):
        return f"<CaseTimeline(id={self.id}, case_id={self.case_id}, event_type={self.event_type}, event_date={self.event_date})>"
