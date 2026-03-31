"""
用户相关的 Pydantic Schemas
用于请求验证和响应序列化
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户姓名")
    email: EmailStr = Field(..., description="邮箱地址")
    role: str = Field(default="staff", description="角色: admin/agent/staff")
    entity: str = Field(default="宝宸", description="主体: 宝宸/瑞宸")
    phone: Optional[str] = Field(None, max_length=50, description="电话")
    agent_number: Optional[str] = Field(None, max_length=50, description="代理师资格证号")


class UserCreate(UserBase):
    """用户创建请求模型"""
    password: str = Field(..., min_length=6, max_length=100, description="密码(6-100位)")


class UserLogin(BaseModel):
    """用户登录请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., description="密码")


class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True  # Pydantic v2: 允许从 ORM 模型创建


class Token(BaseModel):
    """令牌响应模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class TokenData(BaseModel):
    """令牌数据模型"""
    user_id: Optional[int] = Field(None, description="用户ID")


class LoginResponse(BaseModel):
    """登录响应模型(包含令牌和用户信息)"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse = Field(..., description="用户信息")
