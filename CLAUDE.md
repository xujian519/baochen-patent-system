# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

宝宸专利管理系统（BaoChen Patent Management System）—— 宝宸专利代理事务所的专利案卷管理系统。未来将有独立的商标管理系统等其他业务系统。

核心设计：以 **cases（案件总表）** 为主表，费用/文件/期限/官方来文/任务为子表关联跟踪。

**当前状态**：Phase 1（v0.01 → v0.10），目标：跑通后端 + 前端 + 数据库。

## 核心设计文档

所有设计和规范定义在 `docs/` 目录下，按优先级：
- `docs/CONSTITUTION.md` — 编程宪法（技术栈、编码规范、架构约束），**不可违反**
- `docs/FEATURES.md` — 功能规格（业务规则、数据库表、API端点、前端页面、角色权限）
- `docs/PLAN.md` — 开发计划（4个Phase、团队分工、质量门禁）

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.11+ / FastAPI / SQLAlchemy 2.0 async / Alembic |
| 数据库 | PostgreSQL 15.x（独立库 `baochen_mgmt`） |
| 前端 | React 18+ / TypeScript / Tailwind CSS / shadcn/ui（Airtable风格） |
| 状态管理 | Zustand |
| 认证 | JWT（自建，bcrypt加密，24h过期） |
| 部署 | Docker Compose / Tailscale内网 |
| AI | OpenClaw API |

## 架构

```
backend/
├── app/
│   ├── main.py, config.py, database.py
│   ├── models/          # SQLAlchemy ORM模型
│   ├── schemas/         # Pydantic v2 数据验证
│   ├── api/v1/          # 路由：cases|clients|fees|documents|deadlines|letters|tasks|auth|stats|pending|ai
│   ├── services/        # 业务逻辑层
│   ├── utils/
│   └── middleware/
├── migrations/          # Alembic
└── tests/

frontend/
├── src/
│   ├── components/      # ui/(shadcn) | grid/(Airtable网格) | form/ | layout/
│   ├── pages/           # 14个页面
│   ├── hooks/
│   ├── stores/          # Zustand
│   ├── api/             # API调用层
│   ├── types/
│   └── utils/
```

**后端四层架构**：API层（路由+验证）→ Service层（业务逻辑）→ Repository层（数据访问）→ Model层（ORM）

## 编码规范

### 通用
- 中文注释，英文变量名/函数名
- Python 4空格缩进，TypeScript 2空格缩进
- 行宽120字符
- 所有配置用环境变量，禁止硬编码

### Python
- PEP 8，async优先，Pydantic v2，FastAPI Depends注入

### TypeScript/React
- 函数组件 + Hooks，禁止 `any`，Props用 `interface`

### 数据库
- 蛇形命名，每表必须有 `id` + `created_at`，外键显式声明，所有变更通过Alembic

### Git
- 分支：main / develop / feature/*
- 提交：`feat: xxx` / `fix: xxx` / `docs: xxx`

## API规范

- 前缀：`/api/v1/`
- 统一响应：`{ "code": 200, "data": ..., "message": "ok" }`
- 错误：`{ "code": 4xx/5xx, "detail": "错误描述" }`
- 分页：`?page=1&page_size=20`

## 关键业务规则

### 案件编号
- 格式：`BCZL + 年月 + 类型(1发明/2实用新型/3外观) + 流水号`，如 `BCZL2026031001`
- 普通用户可修改1次，admin（徐健）可修改多次

### 案件状态流转
`新案 → 撰写中 → 待质检 → 已定稿 → 待递交 → 已递交/在审 → 答复OA → 授权/驳回 → 结案归档`

### 期限预警（3级）
- 一级：到期前15天
- 二级：到期前7天
- 三级：到期前3天（升级通知）

### 角色权限
- **admin**（徐健）：全部权限 + 编号多次修改 + 用户管理
- **operator**（孙艳玲等）：案件CRUD + 编号改1次 + AI识别 + 待确认编辑（自己的）
- **readonly**：只读 + 数据导出

## 数据库（10张表）

`clients` → `cases`（主表）← `fees` / `documents` / `deadlines` / `official_letters` / `case_timeline` / `tasks`。另有 `file_locations`（文件目录树）和 `users`。官文类型枚举38+1种，详见 `docs/FEATURES.md`。

## 开发命令（项目初始化后）

```bash
# 后端
cd backend
pip install -r requirements.txt
alembic upgrade head          # 数据库迁移
pytest                        # 后端测试
uvicorn app.main:app --reload # 本地开发

# 前端
cd frontend
npm install
npm run dev                   # 本地开发
npm run build                 # 构建

# Docker
docker-compose up --build     # 容器化部署
```
