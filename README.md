# 宝宸专利管理系统

专利案卷全生命周期管理平台，为专利代理事务所提供高效的案件管理、客户管理、费用跟踪等服务。

## 功能特性

### MVP v0.1.0（当前版本）
- ✅ 用户认证（JWT 登录）
- ✅ 案件管理（创建、列表、编辑）
- ✅ 客户管理（创建、列表、编辑）
- ✅ 智能输入（支持选择已有记录或自定义输入）

### 规划功能
- 📋 费用管理（应收、应付、开票跟踪）
- 📁 文件管理（案件文档上传与分类）
- ⏰ 期限管理（自动预警与提醒）
- 📨 官方来文管理（38+ 种官文类型）
- 📊 统计报表（业务数据分析）
- 🤖 AI 功能（智能分类、自动填充）

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11 / FastAPI / SQLAlchemy 2.0 async |
| 数据库 | PostgreSQL 15 |
| 前端 | React 18 / TypeScript / Tailwind CSS / shadcn/ui |
| 状态管理 | Zustand |
| 认证 | JWT（24h 过期） |
| 部署 | Docker Compose |

## 快速开始

### 环境要求
- Docker & Docker Compose
- Git

### 一键部署

```bash
# 克隆仓库
git clone https://github.com/xujian519/baochen-patent-system.git
cd baochen-patent-system

# 复制环境变量配置
cp .env.example .env

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |

### 默认账号

- 邮箱：`admin@baochen.com`
- 密码：`admin123`

## 项目结构

```
baochen-patent-system/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/v1/         # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 验证
│   │   ├── services/       # 业务逻辑
│   │   └── middleware/     # 中间件
│   ├── migrations/         # 数据库迁移
│   └── requirements.txt
├── frontend/               # 前端服务
│   ├── src/
│   │   ├── api/           # API 调用
│   │   ├── components/    # UI 组件
│   │   ├── pages/         # 页面
│   │   ├── stores/        # 状态管理
│   │   └── types/         # 类型定义
│   └── package.json
├── docker-compose.yml      # Docker 编排
└── docs/                   # 设计文档
```

## 开发指南

### 本地开发

**后端**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**前端**
```bash
cd frontend
npm install
npm run dev
```

### 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | `POST /api/v1/auth/login` | 用户登录 |
| 案件 | `GET /api/v1/cases/` | 案件列表 |
| 案件 | `POST /api/v1/cases/` | 创建案件 |
| 客户 | `GET /api/v1/clients/` | 客户列表 |
| 用户 | `GET /api/v1/users/` | 用户列表 |

完整 API 文档：http://localhost:8000/docs

## 核心业务规则

### 案件编号规则
- 格式：`BCZL` + 年月 + 类型码 + 流水号
- 类型码：1=发明，2=实用新型，3=外观设计
- 示例：`BCZL2026031001`

### 案件状态流转
```
新案 → 撰写中 → 待质检 → 已定稿 → 待递交 → 已递交/在审 → 答复OA → 授权/驳回 → 结案归档
```

### 角色权限
| 角色 | 权限 |
|------|------|
| admin | 全部权限 + 用户管理 |
| operator | 案件 CRUD + AI 功能 |
| readonly | 只读 + 数据导出 |

## 设计文档

详细设计文档位于 `docs/` 目录：
- `CONSTITUTION.md` - 编程宪法（技术规范）
- `FEATURES.md` - 功能规格（业务规则）
- `PLAN.md` - 开发计划（里程碑）

## 技术支持

- 作者：徐健
- 邮箱：xujian519@gmail.com

## 许可证

MIT License
