# 宝宸专利管理系统 - 后端

基于 FastAPI + SQLAlchemy 2.0 async + PostgreSQL 的后端服务。

## 技术栈

- Python 3.11+
- FastAPI - Web框架
- SQLAlchemy 2.0 (async) - ORM
- Alembic - 数据库迁移
- PostgreSQL 15.x - 数据库
- Pydantic - 数据验证

## 目录结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   └── models/              # 数据模型
│       ├── __init__.py
│       ├── base.py
│       ├── user.py
│       ├── client.py
│       ├── case.py
│       ├── fee.py
│       ├── document.py
│       ├── file_location.py
│       ├── deadline.py
│       ├── letter.py
│       ├── timeline.py
│       └── task.py
├── migrations/              # Alembic迁移
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

## 快速开始

### 1. 创建虚拟环境

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接：

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/baochen_mgmt
JWT_SECRET_KEY=your-super-secret-key
```

### 4. 创建数据库

确保 PostgreSQL 已运行，然后创建数据库：

```bash
psql -U postgres
CREATE DATABASE baochen_mgmt;
\q
```

### 5. 运行数据库迁移

```bash
alembic upgrade head
```

### 6. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用Python直接运行
python -m uvicorn app.main:app --reload
```

### 7. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 数据库模型

### 核心表

1. **users** - 系统用户（管理员、代理师、员工）
2. **clients** - 客户信息
3. **cases** - 案件总表（主表）
4. **fees** - 费用记录
5. **documents** - 文件管理
6. **file_locations** - 文件夹结构
7. **deadlines** - 期限管理（3级预警）
8. **official_letters** - 官方来文
9. **case_timeline** - 案件时间线
10. **tasks** - 任务管理

## API端点（待实现）

后续Agent将实现以下路由：

- `/api/v1/auth` - 认证相关
- `/api/v1/cases` - 案件管理
- `/api/v1/clients` - 客户管理
- `/api/v1/fees` - 费用管理
- `/api/v1/documents` - 文件管理
- `/api/v1/deadlines` - 期限管理
- `/api/v1/letters` - 官文管理
- `/api/v1/tasks` - 任务管理
- `/api/v1/stats` - 统计报表
- `/api/v1/ai` - AI功能

## 数据库迁移命令

```bash
# 查看当前版本
alembic current

# 查看迁移历史
alembic history

# 生成新迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚上一版本
alembic downgrade -1

# 回滚所有
alembic downgrade base
```

## 开发规范

- 中文注释，英文变量名
- Python 4空格缩进，行宽120
- SQLAlchemy 2.0 async模式
- 蛇形命名（表名、列名）
- 所有模型必须有 `__repr__` 方法

## 许可证

私有项目 - 宝宸专利管理系统
