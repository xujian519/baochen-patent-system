# 认证系统 API 文档

## 概述

宝宸专利管理系统的用户认证系统基于 JWT (JSON Web Token) 实现,提供用户注册、登录、令牌验证等功能。

## 技术栈

- **FastAPI**: 现代高性能 Web 框架
- **JWT**: python-jose 库实现令牌生成和验证
- **密码加密**: passlib + bcrypt 算法
- **数据库**: PostgreSQL + SQLAlchemy 2.0 async

## API 端点

### 1. 用户注册

**POST** `/api/v1/auth/register`

创建新用户账号。

**请求体**:
```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "password": "password123",
  "role": "admin",
  "entity": "宝宸",
  "phone": "13800138000",
  "agent_number": "123456"
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "role": "admin",
  "entity": "宝宸",
  "phone": "13800138000",
  "agent_number": "123456",
  "is_active": true,
  "created_at": "2026-03-31T10:00:00"
}
```

### 2. 用户登录

**POST** `/api/v1/auth/login`

使用邮箱和密码登录,返回 JWT 令牌。

**请求体**:
```json
{
  "email": "zhangsan@example.com",
  "password": "password123"
}
```

**响应** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "role": "admin",
    "entity": "宝宸",
    "phone": "13800138000",
    "agent_number": "123456",
    "is_active": true,
    "created_at": "2026-03-31T10:00:00"
  }
}
```

### 3. 获取当前用户信息

**GET** `/api/v1/auth/me`

获取当前认证用户的详细信息。

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应** (200 OK):
```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "role": "admin",
  "entity": "宝宸",
  "phone": "13800138000",
  "agent_number": "123456",
  "is_active": true,
  "created_at": "2026-03-31T10:00:00"
}
```

## 认证流程

1. **注册**: 用户通过 `/register` 端点创建账号,密码使用 bcrypt 加密存储
2. **登录**: 用户通过 `/login` 端点提交凭据,验证通过后返回 JWT 令牌
3. **访问受保护资源**: 在请求头中携带令牌 `Authorization: Bearer <token>`
4. **令牌验证**: 中间件自动验证令牌,提取用户信息

## 角色权限

系统支持三种角色:
- **admin**: 管理员,拥有所有权限
- **agent**: 代理师,可以管理案件和客户
- **staff**: 员工,基础权限

## 使用示例

### Python (requests)
```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "zhangsan@example.com",
        "password": "password123"
    }
)
data = response.json()
token = data["access_token"]

# 获取用户信息
headers = {"Authorization": f"Bearer {token}"}
user_info = requests.get(
    "http://localhost:8000/api/v1/auth/me",
    headers=headers
)
print(user_info.json())
```

### JavaScript (fetch)
```javascript
// 登录
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'zhangsan@example.com',
    password: 'password123'
  })
});
const { access_token } = await loginResponse.json();

// 获取用户信息
const userResponse = await fetch('http://localhost:8000/api/v1/auth/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const user = await userResponse.json();
console.log(user);
```

## 安全措施

1. **密码加密**: 使用 bcrypt 算法加密存储密码
2. **JWT 签名**: 使用 HS256 算法签名令牌
3. **令牌过期**: 默认 24 小时过期
4. **CORS 配置**: 可配置允许的来源
5. **用户状态检查**: 验证用户是否被禁用

## 配置项

在 `.env` 文件中配置:
```env
# JWT配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/baochen_mgmt
```

## 错误处理

- **400 Bad Request**: 邮箱已被注册、请求参数错误
- **401 Unauthorized**: 邮箱或密码错误、令牌无效
- **403 Forbidden**: 用户已被禁用、权限不足

## 测试

运行测试脚本:
```bash
cd backend
python test_auth.py
```

测试覆盖:
- ✅ 用户注册
- ✅ 密码加密验证
- ✅ 用户登录
- ✅ 错误密码拒绝
- ✅ JWT 令牌生成
- ✅ 令牌验证
- ✅ 重复注册拒绝
