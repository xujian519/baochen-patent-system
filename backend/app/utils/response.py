"""
统一响应格式工具
提供标准化的 API 响应格式
"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


class ApiResponse:
    """统一 API 响应格式"""

    @staticmethod
    def success(
        data: Any = None,
        message: str = "ok",
        code: int = 200
    ) -> dict:
        """
        成功响应

        Args:
            data: 响应数据
            message: 响应消息
            code: 状态码

        Returns:
            dict: 标准格式的响应
        """
        return {
            "code": code,
            "data": data,
            "message": message
        }

    @staticmethod
    def error(
        detail: str,
        code: int = 400,
        data: Optional[Any] = None
    ) -> dict:
        """
        错误响应

        Args:
            detail: 错误详情
            code: 错误状态码
            data: 额外数据(可选)

        Returns:
            dict: 标准格式的错误响应
        """
        return {
            "code": code,
            "detail": detail,
            "data": data
        }
