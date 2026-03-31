"""
JWT令牌处理模块
使用 python-jose 生成和验证 JWT token
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

from app.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌

    Args:
        data: 要编码到令牌中的数据(通常是 {"sub": user_id})
        expires_delta: 过期时间增量,如果为 None 则使用默认配置

    Returns:
        str: JWT 令牌字符串
    """
    # 复制数据以避免修改原始字典
    to_encode = data.copy()
    # jose 要求 sub 必须是字符串
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])

    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    # 添加过期时间到载荷
    to_encode.update({"exp": expire})

    # 编码 JWT 令牌
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码并验证 JWT 访问令牌

    Args:
        token: JWT 令牌字符串

    Returns:
        Optional[Dict[str, Any]]: 解码后的载荷数据,如果验证失败返回 None
    """
    try:
        # 解码 JWT 令牌
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        # 令牌无效或已过期
        return None
