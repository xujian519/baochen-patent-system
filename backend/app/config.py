"""
配置管理模块
使用 pydantic-settings 从环境变量读取配置
"""
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """应用配置"""

    # 数据库配置
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/baochen_mgmt"

    # JWT配置
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24小时

    # CORS 配置
    cors_origins: str = "http://localhost:3000,http://localhost"

    # 应用配置
    app_name: str = "宝宸专利管理系统"
    app_version: str = "0.1.0"
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
settings = Settings()
