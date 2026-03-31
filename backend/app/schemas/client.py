"""
客户相关的 Pydantic Schemas
用于 API 请求验证和响应序列化
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    """客户基础模型"""
    name: str = Field(..., max_length=200, description="客户名称")
    short_name: Optional[str] = Field(None, max_length=100, description="客户简称")
    contact_person: Optional[str] = Field(None, max_length=100, description="联系人")
    phone: Optional[str] = Field(None, max_length=50, description="电话")
    email: Optional[str] = Field(None, max_length=200, description="邮箱")
    address: Optional[str] = Field(None, description="地址")
    type: str = Field(default="企业", max_length=20, description="类型: 企业/个人")
    credit_code: Optional[str] = Field(None, max_length=50, description="统一社会信用代码")
    fee_reduction: bool = Field(default=False, description="是否费减")
    notes: Optional[str] = Field(None, description="备注")

    class Config:
        from_attributes = True


class ClientCreate(ClientBase):
    """创建客户请求模型"""
    pass


class ClientUpdate(BaseModel):
    """更新客户请求模型 - 所有字段可选"""
    name: Optional[str] = Field(None, max_length=200, description="客户名称")
    short_name: Optional[str] = Field(None, max_length=100, description="客户简称")
    contact_person: Optional[str] = Field(None, max_length=100, description="联系人")
    phone: Optional[str] = Field(None, max_length=50, description="电话")
    email: Optional[str] = Field(None, max_length=200, description="邮箱")
    address: Optional[str] = Field(None, description="地址")
    type: Optional[str] = Field(None, max_length=20, description="类型: 企业/个人")
    credit_code: Optional[str] = Field(None, max_length=50, description="统一社会信用代码")
    fee_reduction: Optional[bool] = Field(None, description="是否费减")
    notes: Optional[str] = Field(None, description="备注")

    class Config:
        from_attributes = True


class ClientResponse(ClientBase):
    """客户响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CaseBriefForClient(BaseModel):
    """案件的简要信息（用于客户关联展示）"""
    id: int
    case_number: str
    title: str
    patent_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClientWithCases(ClientResponse):
    """客户详情（含关联案件）"""
    cases: List[CaseBriefForClient] = []

    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    """客户列表响应"""
    items: List[ClientResponse]
    total: int
    page: int
    page_size: int

    class Config:
        from_attributes = True
