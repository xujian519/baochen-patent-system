# 认证系统快速参考

## 核心文件位置

```
backend/
├── app/
│   ├── api/v1/auth.py              # API 路由: 注册、登录、获取用户
│   ├── middleware/auth.py          # 认证依赖: get_current_user, require_role
│   ├── services/auth.py            # 业务逻辑: register, authenticate, get_current_user
│   ├── schemas/user.py             # 数据模型: UserCreate, UserLogin, UserResponse
│   └── utils/
│       ├── security.py             # 密码加密: verify_password, get_password_hash
│       ├── jwt_handler.py          # JWT处理: create_access_token, decode_access_token
│       └── response.py             # 统一响应: ApiResponse.success, ApiResponse.error
```

## API 端点

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| POST | /api/v1/auth/register | 用户注册 | ❌ |
| POST | /api/v1/auth/login | 用户登录 | ❌ |
| GET | /api/v1/auth/me | 获取当前用户 | ✅ |

## 使用认证保护端点

```python
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_active_user, require_admin
from app.models.user import User

router = APIRouter()

# 需要登录
@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"user": current_user.name}

# 需要管理员角色
@router.delete("/admin-only")
async def admin_route(current_user: User = Depends(require_admin)):
    return {"message": "Admin access granted"}
```

## 快速测试命令

### 1. 注册用户
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试用户",
    "email": "test@example.com",
    "password": "password123",
    "role": "admin",
    "entity": "宝宸"
  }'
```

### 2. 登录获取令牌
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. 使用令牌访问受保护资源
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## 角色权限

| 角色 | 代码 | 权限级别 |
|------|------|----------|
| 管理员 | admin | 全部权限 |
| 代理师 | agent | 案件、客户管理 |
| 员工 | staff | 基础权限 |

### 使用角色检查
```python
from app.middleware.auth import require_admin, require_agent, require_staff

# 只允许管理员
@router.delete("/users/{user_id}")
async def delete_user(user: User = Depends(require_admin)):
    pass

# 允许管理员和代理师
@router.put("/cases/{case_id}")
async def update_case(user: User = Depends(require_agent)):
    pass

# 允许所有员工
@router.get("/cases")
async def list_cases(user: User = Depends(require_staff)):
    pass

# 自定义角色检查
from app.middleware.auth import require_role

@router.post("/special")
async def special_action(user: User = Depends(require_role(["admin", "agent"]))):
    pass
```

## 常见问题

### Q: 令牌过期时间是多少?
A: 默认 1440 分钟(24小时),可在 `.env` 中配置 `ACCESS_TOKEN_EXPIRE_MINUTES`

### Q: 如何修改 JWT 密钥?
A: 在 `.env` 中设置 `JWT_SECRET_KEY`,生产环境务必使用强密钥

### Q: 密码如何加密?
A: 使用 bcrypt 算法,自动加盐,单向加密

### Q: 如何处理认证失败?
A: 中间件会自动返回 401 Unauthorized 或 403 Forbidden

### Q: 如何在代码中创建令牌?
```python
from app.services.auth import AuthService

token = AuthService.create_user_token(user_id=1)
```

### Q: 如何在代码中验证密码?
```python
from app.utils.security import verify_password

is_valid = verify_password(plain_password, hashed_password)
```

## 启动服务

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量 (.env)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/baochen_mgmt
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 3. 运行数据库迁移
alembic upgrade head

# 4. 启动服务
uvicorn app.main:app --reload

# 5. 访问 API 文档
# http://localhost:8000/docs
```

## 运行测试

```bash
python test_auth.py
```

## 下一步

- [ ] 实现刷新令牌
- [ ] 添加密码重置功能
- [ ] 实现邮箱验证
- [ ] 添加审计日志
- [ ] 实施 API 限流
