"""
基础模型类
提供通用的字段和方法
"""
from datetime import datetime
from sqlalchemy import Column, DateTime

# 从 database.py 导入统一的 Base，确保所有模型使用同一个 Base
from app.database import Base


class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
