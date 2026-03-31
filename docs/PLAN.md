# 宝宸专利管理系统 - 开发计划 v0.01

> 本文件定义开发阶段和分工，Claude Code 按此执行。

---

## 团队分工

| 角色 | 谁来做 | 职责 |
|------|--------|------|
| **编程** | Claude Code | 按CONSTITUTION.md + FEATURES.md编码 |
| **代码审查** | 云熙 | 审查代码质量、规范合规、架构合理性 |
| **测试** | 小诺 | 功能测试、API测试、端到端测试 |
| **决策** | 爸爸（徐健） | 最终审批、需求确认 |

---

## 开发阶段

### Phase 1: 基础骨架（v0.01 → v0.10）⭐ 当前

**目标**：跑通后端 + 前端 + 数据库

#### 并行开发安排（5个子智能体）

```
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 1 并行开发                          │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│  Agent-1    │  Agent-2    │  Agent-3    │  Agent-4    │ Agent-5 │
│  后端基础   │  认证系统   │  案件业务   │  前端基础   │ 案件UI  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                              ↓
                    ┌─────────────────┐
                    │   最终整合      │
                    │   Docker部署    │
                    └─────────────────┘
```

---

#### Agent-1: 后端基础设施 🏗️

**职责**：搭建后端骨架和数据库

| 任务 | 说明 | 产出 |
|------|------|------|
| FastAPI项目初始化 | 目录结构、依赖管理 | `backend/` 目录 |
| 配置管理 | 环境变量、config.py | `app/config.py` |
| 数据库连接 | SQLAlchemy async 配置 | `app/database.py` |
| 10张表模型 | 按FEATURES.md定义 | `app/models/*.py` |
| Alembic迁移 | 初始化 + 首次迁移 | `migrations/` |

**关键文件**：
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── models/
│       ├── __init__.py
│       ├── base.py
│       ├── user.py
│       ├── client.py
│       ├── case.py
│       ├── fee.py
│       ├── document.py
│       ├── deadline.py
│       ├── letter.py
│       ├── timeline.py
│       └── task.py
├── migrations/
├── requirements.txt
└── .env.example
```

**验收标准**：`alembic upgrade head` 成功，PG中可见10张表

---

#### Agent-2: 认证系统 🔐

**职责**：用户认证和权限控制

**依赖**：Agent-1 完成（users表存在）

| 任务 | 说明 | 产出 |
|------|------|------|
| 密码加密 | bcrypt实现 | `app/utils/security.py` |
| JWT工具 | 生成/验证Token | `app/utils/jwt.py` |
| 用户Schema | Pydantic模型 | `app/schemas/user.py` |
| 注册API | POST /api/v1/auth/register | `app/api/v1/auth.py` |
| 登录API | POST /api/v1/auth/login |
| 当前用户 | GET /api/v1/auth/me |
| 认证中间件 | Depends注入 | `app/middleware/auth.py` |

**关键文件**：
```
backend/app/
├── schemas/
│   └── user.py
├── utils/
│   ├── security.py
│   └── jwt.py
├── middleware/
│   └── auth.py
└── api/v1/
    └── auth.py
```

**验收标准**：能注册、登录、获取当前用户，JWT验证通过

---

#### Agent-3: 案件核心业务 📋

**职责**：案件和客户的完整CRUD

**依赖**：Agent-1 完成（cases/clients表存在）

| 任务 | 说明 | 产出 |
|------|------|------|
| 客户Schema | Pydantic模型 | `app/schemas/client.py` |
| 案件Schema | Pydantic模型 | `app/schemas/case.py` |
| 编号生成器 | BCZL + 年月 + 类型 + 流水号 | `app/services/numbering.py` |
| 客户Service | 业务逻辑 | `app/services/client.py` |
| 案件Service | 业务逻辑 + 状态流转 | `app/services/case.py` |
| 客户API | CRUD端点 | `app/api/v1/clients.py` |
| 案件API | CRUD + 状态更新 | `app/api/v1/cases.py` |

**关键文件**：
```
backend/app/
├── schemas/
│   ├── client.py
│   └── case.py
├── services/
│   ├── numbering.py
│   ├── client.py
│   └── case.py
└── api/v1/
    ├── clients.py
    └── cases.py
```

**验收标准**：
- 客户CRUD正常
- 案件自动编号正确（BCZL2026031001）
- 案件状态流转记录到timeline

---

#### Agent-4: 前端基础设施 🖥️

**职责**：前端骨架和登录流程

| 任务 | 说明 | 产出 |
|------|------|------|
| React项目初始化 | Vite + TypeScript | `frontend/` 目录 |
| Tailwind配置 | 按shadcn/ui要求 | `tailwind.config.js` |
| shadcn/ui安装 | 基础组件库 | `src/components/ui/` |
| 路由配置 | React Router | `src/router.tsx` |
| API封装 | Axios + Token注入 | `src/api/client.ts` |
| 登录页 | 表单 + 调用API | `src/pages/Login.tsx` |
| 主布局 | 左侧导航 + 顶部工具栏 | `src/components/layout/` |
| Auth Store | Zustand状态 | `src/stores/auth.ts` |

**关键文件**：
```
frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── router.tsx
│   ├── api/
│   │   └── client.ts
│   ├── components/
│   │   ├── ui/           # shadcn组件
│   │   └── layout/
│   │       ├── MainLayout.tsx
│   │       ├── Sidebar.tsx
│   │       └── Header.tsx
│   ├── pages/
│   │   └── Login.tsx
│   └── stores/
│       └── auth.ts
├── package.json
├── tailwind.config.js
└── .env.example
```

**验收标准**：
- `npm run dev` 启动成功
- 登录页可正常显示
- 登录成功后跳转到主页布局

---

#### Agent-5: 案件前端页面 📊

**职责**：案件管理的完整UI

**依赖**：Agent-4 完成（布局和API封装）

| 任务 | 说明 | 产出 |
|------|------|------|
| 案件Store | Zustand状态管理 | `src/stores/case.ts` |
| 案件API | 调用后端接口 | `src/api/cases.ts` |
| 客户API | 调用后端接口 | `src/api/clients.ts` |
| 案件列表页 | Airtable风格网格 | `src/pages/Cases/List.tsx` |
| 数据网格组件 | 可内联编辑 | `src/components/grid/DataTable.tsx` |
| 案件详情抽屉 | 右侧滑出 | `src/pages/Cases/Detail.tsx` |
| 案件表单 | 新建/编辑 | `src/pages/Cases/Form.tsx` |
| 客户选择器 | 搜索+选择组件 | `src/components/form/ClientSelect.tsx` |

**关键文件**：
```
frontend/src/
├── api/
│   ├── cases.ts
│   └── clients.ts
├── components/
│   ├── grid/
│   │   └── DataTable.tsx
│   └── form/
│       └── ClientSelect.tsx
├── pages/
│   └── Cases/
│       ├── List.tsx
│       ├── Detail.tsx
│       └── Form.tsx
└── stores/
    └── case.ts
```

**验收标准**：
- 案件列表可显示、分页、排序
- 点击行可查看详情（右侧抽屉）
- 可新建/编辑案件，自动生成编号

---

#### 最终整合 & 部署 🚀

**依赖**：Agent 1-5 全部完成

| 任务 | 说明 |
|------|------|
| API集成测试 | 前后端联调 |
| Docker Compose | PG + backend + frontend |
| 环境变量配置 | .env文件 |
| Tailscale配置 | 内网访问 |

**验收标准**：
- `docker-compose up` 一键启动
- 能登录、能建案件、能列表查看、能编辑

---

#### 时间线 & 里程碑

```
Day 1-2:  Agent-1 后端基础 + Agent-4 前端基础（并行）
Day 2-3:  Agent-2 认证系统（依赖Agent-1）
Day 2-3:  Agent-5 案件UI开发（依赖Agent-4）
Day 3-4:  Agent-3 案件业务（依赖Agent-1）
Day 4-5:  最终整合 + Docker部署
```

**交付标准**：能登录、能建案件、能列表查看、能编辑

---

### Phase 2: 核心业务（v0.11 → v0.20）

**目标**：费用/文件/期限/官文/任务全部可用

- [ ] 费用 CRUD API + 前端页面
- [ ] 文件上传/下载（自动命名 + 文件夹树自动创建）
- [ ] 期限管理 + 3级预警（Cron定时检查）
- [ ] 官方来文管理
- [ ] 任务管理（看板视图）
- [ ] 待确认队列
- [ ] 客户详情页（关联案件/费用汇总）
- [ ] 案件时间线自动记录

---

### Phase 3: AI集成（v0.21 → v0.30）

**目标**：OpenClaw深度集成

- [ ] AI识别接口（PDF → 结构化数据）
- [ ] OpenClaw双向对接（小诺调用API操作数据）
- [ ] 自然语言查询
- [ ] 文件自动识别 + 复制到对应文件夹
- [ ] 自动提醒推送到飞书/微信/iMessage
- [ ] 仪表盘统计

---

### Phase 4: 优化上线（v0.31 → v1.00）

**目标**：生产就绪

- [ ] 历史数据迁移（从Excel模板导入）
- [ ] 权限细化（admin/operator/readonly）
- [ ] 数据备份自动化
- [ ] 移动端优化
- [ ] 性能优化
- [ ] 全面测试 + Bug修复
- [ ] 文档编写（使用说明）

---

## 版本号规则

- 当前：v0.01
- 每完成一个功能点（可演示）：+0.01
- Phase 1 完成：v0.10
- Phase 2 完成：v0.20
- Phase 3 完成：v0.30
- Phase 4 完成 → 测试通过：v1.00 正式上线

---

## 质量门禁

每个 Phase 完成后：

1. **Claude Code** 完成编码 → 提交PR
2. **云熙** 审查代码质量 → 通过/打回
3. **小诺** 执行测试 → 通过/记录Bug
4. **爸爸** 最终确认 → 进入下一Phase

任何一环不通过，回退修复。

---

*本计划由小诺编写，爸爸批准后生效。*
