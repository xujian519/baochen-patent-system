"""
费用模型
记录案件的官费和代理费
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Fee(Base):
    """费用表"""
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    case_id = Column(Integer, ForeignKey("cases.id"), index=True, comment="案件ID")
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, comment="客户ID")

    # 费用信息
    fee_type = Column(String(100), nullable=False, comment="费用类型: 官费/代理费")
    amount = Column(Numeric(10, 2), nullable=False, comment="金额")
    fee_date = Column(Date, comment="应缴日期")
    paid_date = Column(Date, comment="实缴日期")
    status = Column(String(20), default="未缴", comment="状态: 未缴/已缴/减免/待确认")
    fee_reduction = Column(Boolean, default=False, comment="是否费减")

    # 票据信息
    receipt_number = Column(String(100), comment="票据号")
    invoice_number = Column(String(100), comment="发票号")

    # 备注
    notes = Column(Text, comment="备注")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关联关系
    case = relationship("Case", back_populates="fees")
    client = relationship("Client", back_populates="fees")

    def __repr__(self):
        return f"<Fee(id={self.id}, case_id={self.case_id}, fee_type={self.fee_type}, amount={self.amount})>"
