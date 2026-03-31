"""
案件模型
案件总表 - 系统的核心主表
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Case(Base):
    """案件总表"""
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True, comment="案件编号: BCZL2026031001")
    entity = Column(String(20), default="宝宸", comment="主体: 宝宸/瑞宸")

    # 客户关联
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, comment="客户ID")

    # 基本信息
    title = Column(String(500), nullable=False, comment="案件名称")
    patent_type = Column(String(20), nullable=False, comment="专利类型: 发明/实用新型/外观设计")
    application_number = Column(String(50), comment="申请号")
    filing_date = Column(Date, comment="申请日（递交国知局日期）")
    publication_number = Column(String(50), comment="公开号")
    grant_number = Column(String(50), comment="授权公告号")
    grant_date = Column(Date, comment="授权日")
    applicant = Column(Text, comment="申请人")
    inventor = Column(Text, comment="发明人")
    patent_holder = Column(String(500), comment="专利权人（可与客户不同）")

    # 人员关联
    agent_id = Column(Integer, ForeignKey("users.id"), comment="代理师ID")
    assistant_id = Column(Integer, ForeignKey("users.id"), comment="协办人ID")
    examiner = Column(String(100), comment="审查员")

    # 状态信息
    stage = Column(String(50), default="新案", comment="案件阶段: 新案/撰写中/待质检/已定稿/待递交/已递交-在审/答复OA/授权/驳回/放弃/结案归档")
    case_status = Column(String(20), default="进行中", comment="案件状态: 进行中/已结案/已终止/已暂停")
    current_stage = Column(String(50), comment="当前节点")

    # 技术信息
    ipc_codes = Column(String(200), comment="IPC分类号")
    tech_field = Column(String(100), comment="技术领域")
    priority_date = Column(Date, comment="优先权日")

    # 期限管理
    nearest_deadline = Column(Date, comment="最近期限")
    deadline_level = Column(Integer, default=0, comment="预警级别 0-3")

    # 财务信息
    quotation_amount = Column(Numeric(10, 2), comment="报价金额")
    fee_reduction_ratio = Column(Integer, default=0, comment="费减比例: 0/70/85/100（百分比）")
    is_contract_signed = Column(Boolean, default=False, comment="是否签合同")

    # 备注
    notes = Column(Text, comment="备注")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="立案日期")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    client = relationship("Client", back_populates="cases")
    agent = relationship("User", back_populates="cases_as_agent", foreign_keys=[agent_id])
    assistant = relationship("User", back_populates="cases_as_assistant", foreign_keys=[assistant_id])
    fees = relationship("Fee", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    file_locations = relationship("FileLocation", back_populates="case", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="case", cascade="all, delete-orphan")
    official_letters = relationship("OfficialLetter", back_populates="case", cascade="all, delete-orphan")
    timelines = relationship("CaseTimeline", back_populates="case", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="case")

    def __repr__(self):
        return f"<Case(id={self.id}, case_number={self.case_number}, title={self.title[:20]}...)>"
