"""
数据库初始化脚本
首次启动时创建初始管理员用户
"""
import asyncio
from sqlalchemy import select

from app.database import async_session_maker
from app.models.user import User
from app.utils.security import get_password_hash


async def create_admin_user():
    """创建初始管理员用户（如果不存在）"""
    async with async_session_maker() as session:
        # 检查是否已存在管理员
        result = await session.execute(
            select(User).where(User.role == "admin")
        )
        admin = result.scalar_one_or_none()

        if admin:
            print("管理员用户已存在，跳过创建")
            return

        # 创建管理员
        admin = User(
            name="徐健",
            email="admin@baochen.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
            entity="宝宸",
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        print("初始管理员用户创建成功")
        print(f"  邮箱: admin@baochen.com")
        print(f"  密码: admin123")
        print("  请登录后立即修改密码！")


async def main():
    print("初始化数据库...")
    await create_admin_user()
    print("数据库初始化完成")


if __name__ == "__main__":
    asyncio.run(main())
