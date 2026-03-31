"""
客户模型
客户信息表，包含企业和个人客户
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class Client(Base):
    """客户表"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="客户名称")
    short_name = Column(String(100), comment="客户简称")
    contact_person = Column(String(100), comment="联系人")
    phone = Column(String(50), comment="电话")
    email = Column(String(200), comment="邮箱")
    address = Column(Text, comment="地址")
    type = Column(String(20), default="企业", comment="类型: 企业/个人")
    credit_code = Column(String(50), comment="统一社会信用代码")
    fee_reduction = Column(Boolean, default=False, comment="是否费减")
    notes = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    cases = relationship("Case", back_populates="client")
    fees = relationship("Fee", back_populates="client")
    tasks = relationship("Task", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name})>"
