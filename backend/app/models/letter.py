"""
官方来文模型
记录专利局发出的各种官方文件
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class OfficialLetter(Base):
    """官方来文表"""
    __tablename__ = "official_letters"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")
    document_id = Column(Integer, ForeignKey("documents.id"), comment="关联文档ID")

    # 官文信息
    letter_type = Column(String(100), nullable=False, comment="官文类型(38+1种)")
    received_date = Column(Date, nullable=False, comment="收到日期")
    official_number = Column(String(100), comment="官文编号")
    deadline_date = Column(Date, comment="答复期限")
    summary = Column(Text, comment="AI摘要")

    # 处理状态
    is_processed = Column(Boolean, default=False, comment="是否已处理")
    processed_date = Column(Date, comment="处理日期")

    # 备注
    notes = Column(Text, comment="备注")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="official_letters")
    document = relationship("Document", back_populates="official_letter")

    def __repr__(self):
        return f"<OfficialLetter(id={self.id}, letter_type={self.letter_type}, received_date={self.received_date})>"
