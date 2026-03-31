"""
文件模型
管理案件相关的所有文件
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Document(Base):
    """文件表"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")
    location_id = Column(Integer, ForeignKey("file_locations.id"), comment="文件位置ID")

    # 文件信息
    doc_type = Column(String(50), nullable=False, comment="文件类型")
    file_name = Column(String(500), nullable=False, comment="文件名")
    file_path = Column(Text, nullable=False, comment="文件路径")
    file_size = Column(Integer, comment="文件大小(字节)")
    version = Column(Integer, default=1, comment="版本号")
    description = Column(Text, comment="描述")

    # AI相关
    ai_extracted = Column(Boolean, default=False, comment="AI是否已提取")
    ai_confidence = Column(Numeric(5, 2), comment="AI置信度(0-100)")

    # 上传信息
    uploaded_by = Column(String(50), comment="上传者")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="documents")
    location = relationship("FileLocation", back_populates="documents")
    official_letter = relationship("OfficialLetter", back_populates="document", uselist=False)

    def __repr__(self):
        return f"<Document(id={self.id}, file_name={self.file_name})>"
