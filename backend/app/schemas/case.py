"""
案件相关的 Pydantic Schemas
用于 API 请求验证和响应序列化
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class CaseBase(BaseModel):
    """案件基础模型"""
    entity: str = Field(default="宝宸", max_length=20, description="主体: 宝宸/瑞宸")
    client_id: Optional[int] = Field(None, description="客户ID（二选一）")
    client_name: Optional[str] = Field(None, max_length=200, description="客户名称（二选一，用于自定义输入）")
    title: str = Field(..., max_length=500, description="发明名称")
    patent_type: str = Field(..., max_length=20, description="专利类型: 发明/实用新型/外观设计")
    application_number: Optional[str] = Field(None, max_length=50, description="申请号")
    filing_date: Optional[date] = Field(None, description="申请日")
    publication_number: Optional[str] = Field(None, max_length=50, description="公开号")
    grant_number: Optional[str] = Field(None, max_length=50, description="授权公告号")
    grant_date: Optional[date] = Field(None, description="授权日")
    applicant: Optional[str] = Field(None, description="申请人")
    inventor: Optional[str] = Field(None, description="发明人")
    agent_id: Optional[int] = Field(None, description="代理师ID")
    agent_name: Optional[str] = Field(None, max_length=100, description="代理师名称（自定义输入）")
    assistant_id: Optional[int] = Field(None, description="协办人ID")
    assistant_name: Optional[str] = Field(None, max_length=100, description="协办人名称（自定义输入）")
    examiner: Optional[str] = Field(None, max_length=100, description="审查员")
    status: str = Field(default="新案", max_length=50, description="状态")
    current_stage: Optional[str] = Field(None, max_length=50, description="当前节点")
    ipc_codes: Optional[str] = Field(None, max_length=200, description="IPC分类号")
    tech_field: Optional[str] = Field(None, max_length=100, description="技术领域")
    priority_date: Optional[date] = Field(None, description="优先权日")
    nearest_deadline: Optional[date] = Field(None, description="最近期限")
    deadline_level: int = Field(default=0, ge=0, le=3, description="预警级别 0-3")
    quotation_amount: Optional[Decimal] = Field(None, description="报价金额")
    is_contract_signed: bool = Field(default=False, description="是否签合同")
    notes: Optional[str] = Field(None, description="备注")

    class Config:
        from_attributes = True


class CaseCreate(CaseBase):
    """创建案件请求模型"""
    # case_number 不需要客户端提供，由系统自动生成
    pass


class CaseUpdate(BaseModel):
    """更新案件请求模型 - 所有字段可选"""
    entity: Optional[str] = Field(None, max_length=20, description="主体: 宝宸/瑞宸")
    client_id: Optional[int] = Field(None, description="客户ID")
    client_name: Optional[str] = Field(None, max_length=200, description="客户名称（自定义输入）")
    title: Optional[str] = Field(None, max_length=500, description="发明名称")
    patent_type: Optional[str] = Field(None, max_length=20, description="专利类型")
    application_number: Optional[str] = Field(None, max_length=50, description="申请号")
    filing_date: Optional[date] = Field(None, description="申请日")
    publication_number: Optional[str] = Field(None, max_length=50, description="公开号")
    grant_number: Optional[str] = Field(None, max_length=50, description="授权公告号")
    grant_date: Optional[date] = Field(None, description="授权日")
    applicant: Optional[str] = Field(None, description="申请人")
    inventor: Optional[str] = Field(None, description="发明人")
    agent_id: Optional[int] = Field(None, description="代理师ID")
    agent_name: Optional[str] = Field(None, max_length=100, description="代理师名称（自定义输入）")
    assistant_id: Optional[int] = Field(None, description="协办人ID")
    assistant_name: Optional[str] = Field(None, max_length=100, description="协办人名称（自定义输入）")
    examiner: Optional[str] = Field(None, max_length=100, description="审查员")
    status: Optional[str] = Field(None, max_length=50, description="状态")
    current_stage: Optional[str] = Field(None, max_length=50, description="当前节点")
    ipc_codes: Optional[str] = Field(None, max_length=200, description="IPC分类号")
    tech_field: Optional[str] = Field(None, max_length=100, description="技术领域")
    priority_date: Optional[date] = Field(None, description="优先权日")
    nearest_deadline: Optional[date] = Field(None, description="最近期限")
    deadline_level: Optional[int] = Field(None, ge=0, le=3, description="预警级别 0-3")
    quotation_amount: Optional[Decimal] = Field(None, description="报价金额")
    is_contract_signed: Optional[bool] = Field(None, description="是否签合同")
    notes: Optional[str] = Field(None, description="备注")

    class Config:
        from_attributes = True


class CaseResponse(CaseBase):
    """案件响应模型"""
    id: int
    case_number: str = Field(..., description="案件编号（系统自动生成）")
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 关联模型的简要信息（必须在 CaseBrief 之前定义）
class ClientBriefForCase(BaseModel):
    """客户的简要信息（用于案件关联展示）"""
    id: int
    name: str
    short_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class UserBriefForCase(BaseModel):
    """用户的简要信息（用于案件关联展示）"""
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class CaseBrief(BaseModel):
    """案件简要信息（用于列表展示）"""
    id: int
    case_number: str
    title: str
    patent_type: str
    status: str
    client_id: int
    client: Optional[ClientBriefForCase] = None
    agent_id: Optional[int] = None
    agent: Optional[UserBriefForCase] = None
    assistant_id: Optional[int] = None
    assistant: Optional[UserBriefForCase] = None
    filing_date: Optional[date] = None
    nearest_deadline: Optional[date] = None
    deadline_level: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class FeeBriefForCase(BaseModel):
    """费用的简要信息"""
    id: int
    fee_type: str
    amount: Decimal
    status: str
    fee_date: Optional[date] = None  # 应缴日期

    class Config:
        from_attributes = True


class DocumentBriefForCase(BaseModel):
    """文档的简要信息"""
    id: int
    doc_type: str
    file_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class DeadlineBriefForCase(BaseModel):
    """期限的简要信息"""
    id: int
    deadline_type: str
    deadline_date: date
    is_completed: bool  # 改为 is_completed

    class Config:
        from_attributes = True


class TimelineBriefForCase(BaseModel):
    """时间线的简要信息"""
    id: int
    event_type: str
    description: str  # 对应模型中的 description 字段
    event_date: date  # 对应模型中的 event_date 字段

    class Config:
        from_attributes = True


class CaseDetail(CaseResponse):
    """案件详情（含关联数据）"""
    client: Optional[ClientBriefForCase] = None
    fees: List[FeeBriefForCase] = []
    documents: List[DocumentBriefForCase] = []
    deadlines: List[DeadlineBriefForCase] = []
    timelines: List[TimelineBriefForCase] = []


class CaseListResponse(BaseModel):
    """案件列表响应"""
    items: List[CaseBrief]
    total: int
    page: int
    page_size: int

    class Config:
        from_attributes = True


class CaseStatusUpdate(BaseModel):
    """案件状态更新请求"""
    status: str = Field(..., description="新状态")
    notes: Optional[str] = Field(None, description="备注说明")

    class Config:
        from_attributes = True
