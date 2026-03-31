"""
文件位置模型
管理案件的文件夹结构
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class FileLocation(Base):
    """文件位置表 - 管理文件夹树结构"""
    __tablename__ = "file_locations"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")
    parent_id = Column(Integer, ForeignKey("file_locations.id"), comment="父目录ID")

    # 路径信息
    path = Column(Text, nullable=False, comment="完整路径")
    folder_name = Column(String(500), nullable=False, comment="文件夹名称")
    level = Column(Integer, default=0, comment="层级深度")
    is_case_root = Column(Boolean, default=False, comment="是否为案件根目录")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="file_locations")
    parent = relationship("FileLocation", remote_side=[id], backref="children")
    documents = relationship("Document", back_populates="location")

    def __repr__(self):
        return f"<FileLocation(id={self.id}, folder_name={self.folder_name}, level={self.level})>"
