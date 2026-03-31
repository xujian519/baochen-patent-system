"""
认证系统测试脚本
用于测试注册、登录、JWT验证功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker, engine, Base
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import verify_password
from app.utils.jwt_handler import decode_access_token


async def test_auth_system():
    """测试认证系统"""
    print("=" * 60)
    print("🧪 开始测试认证系统")
    print("=" * 60)

    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as db:
        try:
            # 测试1: 用户注册
            print("\n📝 测试1: 用户注册")
            user_data = UserCreate(
                name="测试用户",
                email="test@example.com",
                password="password123",
                role="admin",
                entity="宝宸",
                phone="13800138000"
            )

            try:
                user = await AuthService.register_user(db, user_data)
                print(f"✅ 注册成功: {user.name} ({user.email})")
                print(f"   - 用户ID: {user.id}")
                print(f"   - 角色: {user.role}")
                print(f"   - 密码已加密: {len(user.password_hash)} 字符")
            except Exception as e:
                print(f"❌ 注册失败: {e}")
                return

            # 测试2: 密码验证
            print("\n🔐 测试2: 密码验证")
            is_valid = verify_password("password123", user.password_hash)
            print(f"   - 正确密码验证: {'✅ 通过' if is_valid else '❌ 失败'}")

            is_invalid = verify_password("wrongpassword", user.password_hash)
            print(f"   - 错误密码验证: {'✅ 拒绝' if not is_invalid else '❌ 通过'}")

            # 测试3: 用户登录
            print("\n🔑 测试3: 用户登录")
            authenticated_user = await AuthService.authenticate_user(
                db,
                "test@example.com",
                "password123"
            )
            if authenticated_user:
                print(f"✅ 登录成功: {authenticated_user.name}")
            else:
                print("❌ 登录失败")
                return

            # 测试4: 错误密码登录
            print("\n🚫 测试4: 错误密码登录")
            failed_auth = await AuthService.authenticate_user(
                db,
                "test@example.com",
                "wrongpassword"
            )
            print(f"   - 结果: {'✅ 正确拒绝' if not failed_auth else '❌ 错误通过'}")

            # 测试5: JWT令牌生成
            print("\n🎫 测试5: JWT令牌生成与验证")
            token = AuthService.create_user_token(user.id)
            print(f"   - 令牌已生成: {token[:50]}...")

            # 解码令牌
            payload = decode_access_token(token)
            if payload and payload.get("sub") == user.id:
                print(f"✅ 令牌验证成功,用户ID: {payload.get('sub')}")
            else:
                print("❌ 令牌验证失败")

            # 测试6: 重复注册
            print("\n🚷 测试6: 重复邮箱注册")
            try:
                duplicate_user = await AuthService.register_user(db, user_data)
                print("❌ 允许重复注册(应该失败)")
            except Exception as e:
                print(f"✅ 正确拒绝重复注册: {str(e)}")

            print("\n" + "=" * 60)
            print("✨ 认证系统测试完成")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ 测试过程中出错: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(test_auth_system())
