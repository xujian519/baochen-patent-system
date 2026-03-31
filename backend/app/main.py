"""
FastAPI 应用入口
宝宸专利管理系统 - 后端服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.config import settings
from app.api.v1 import auth_router, clients_router, cases_router, users_router

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="宝宸专利管理系统后端API - 支持案件管理、客户管理、费用管理、文件管理、期限管理等功能",
    debug=settings.debug,
    )

# 从配置解析 CORS 源
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查端点
    用于负载均衡和监控
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/", tags=["根路径"])
async def root():
    """
    根路径 - 欢迎信息
    """
    return {
        "message": f"欢迎访问 {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


# 应用生命周期事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print(f"🚀 {settings.app_name} v{settings.app_version} 启动中...")
    print(f"📊 数据库: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'configured'}")
    print(f"📚 API文档: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print(f"👋 {settings.app_name} 正在关闭...")


# 注册API路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(cases_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
