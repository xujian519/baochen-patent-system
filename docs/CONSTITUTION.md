# 宝宸管理系统 - 编程宪法 v0.01

> 本文件是 Claude Code 开发的最高指导原则，所有代码必须遵守。

---

## 一、项目身份

- **项目名称**：宝宸专利管理系统（BaoChen Patent Management System）
- **版本**：v0.01（每迭代+0.01，v1.00正式上线）
- **定位**：宝宸专利代理事务所的专利案卷管理系统
- **扩展规划**：未来将有独立的商标管理系统等其他业务系统，各系统独立设计
- **核心原则**：以**案件总表**为主表，费用+文件+期限+官方来文+任务为子表关联跟踪

## 二、技术栈（不可更改）

| 层 | 技术 | 版本 |
|----|------|------|
| 后端 | Python + FastAPI | Python 3.11+, FastAPI 最新 |
| 数据库 | PostgreSQL | 15.x |
| ORM | SQLAlchemy 2.0 | async模式 |
| 迁移 | Alembic | 最新 |
| 前端 | React + TypeScript | React 18+ |
| UI框架 | Tailwind CSS + shadcn/ui | Airtable风格 |
| 认证 | JWT（自建） | — |
| 部署 | Docker Compose | — |
| 网络 | Tailscale内网 | — |
| AI集成 | OpenClaw API | — |

## 三、编码规范

### 3.1 通用
- 所有代码中文注释，变量名/函数名用英文
- 文件编码：UTF-8
- 缩进：4空格（Python），2空格（TypeScript）
- 行宽：120字符
- 类型注解：Python用type hints，TypeScript严格模式

### 3.2 Python
- 遵循 PEP 8
- 异步优先（async/await）
- Pydantic v2 做数据验证
- 使用 dependency injection（FastAPI的Depends）

### 3.3 TypeScript/React
- 函数组件 + Hooks
- 禁止 any 类型
- Props 用 interface 定义
- 状态管理：Zustand（轻量）

### 3.4 数据库
- 表名：蛇形命名（snake_case）
- 列名：蛇形命名
- 每张表必须有 id、created_at
- 外键必须显式声明
- 所有变更通过 Alembic 迁移

### 3.5 API
- RESTful 风格
- 统一响应格式：`{ "code": 200, "data": ..., "message": "ok" }`
- 错误格式：`{ "code": 4xx/5xx, "detail": "错误描述" }`
- 分页：`?page=1&page_size=20`
- 版本前缀：`/api/v1/`

## 四、架构约束

### 4.1 目录结构
```
backend/
├── app/
│   ├── main.py              # FastAPI入口
│   ├── config.py             # 配置
│   ├── database.py           # 数据库连接
│   ├── models/               # SQLAlchemy模型
│   ├── schemas/              # Pydantic schemas
│   ├── api/                  # API路由
│   │   ├── v1/
│   │   │   ├── cases.py
│   │   │   ├── clients.py
│   │   │   ├── fees.py
│   │   │   ├── documents.py
│   │   │   ├── deadlines.py
│   │   │   ├── letters.py
│   │   │   ├── tasks.py
│   │   │   ├── auth.py
│   │   │   └── stats.py
│   ├── services/             # 业务逻辑
│   ├── utils/                # 工具函数
│   └── middleware/            # 中间件
├── migrations/               # Alembic迁移
├── tests/                    # 测试
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── components/           # 通用组件
│   │   ├── ui/               # shadcn/ui组件
│   │   ├── grid/             # Airtable风格网格
│   │   ├── form/             # 表单组件
│   │   └── layout/           # 布局
│   ├── pages/                # 页面
│   ├── hooks/                # 自定义hooks
│   ├── stores/               # Zustand stores
│   ├── api/                  # API调用
│   ├── types/                # 类型定义
│   └── utils/                # 工具
├── package.json
└── Dockerfile
```

### 4.2 分层架构
```
API层（路由+参数验证）
    ↓
Service层（业务逻辑）
    ↓
Repository层（数据访问）
    ↓
Model层（ORM模型）
```

### 4.3 禁止事项
- ❌ 禁止直接在API层写SQL
- ❌ 禁止在前端直接调用数据库
- ❌ 禁止硬编码配置（必须用环境变量）
- ❌ 禁止提交敏感信息（密码、密钥等）
- ❌ 禁止跳过数据库迁移直接改表

## 五、安全规范

- JWT Token 认证，过期时间24小时
- 密码 bcrypt 加密
- CORS 限制为 Tailscale 网段
- 所有输入必须验证（Pydantic）
- SQL注入防护（SQLAlchemy ORM天然防护）
- 文件上传限制类型和大小

## 六、AI使用规范

### 6.1 操作确认原则
AI在执行以下操作前，**必须**得到操作人员的明确确认：
- 新建：案件、客户、费用、任务等数据记录
- 编辑：修改任何已存在的数据
- 删除：删除任何数据记录
- 批量操作：涉及多条记录的操作
- 不可逆操作：数据库迁移、结构变更等

**执行方式**：AI 提出操作建议 → 展示具体变更内容 → 等待用户确认 → 执行操作

### 6.2 禁止幻觉原则
AI **严格禁止**产生幻觉，一切输出必须基于：
- 本项目文档（CONSTITUTION.md、FEATURES.md、PLAN.md）
- 用户明确提供的输入信息
- 已定义的业务流程和规则
- 数据库中实际存在的数据

**禁止行为**：
- ❌ 编造不存在的API端点或数据结构
- ❌ 臆测未明确规定的业务规则
- ❌ 假设用户未提供的信息
- ❌ 跳过文档直接按"常识"实现

**遇到不确定时**：必须向用户询问确认，不得自行假设。

## 七、测试规范

- 后端：pytest + httpx（API测试）
- 覆盖率目标：≥ 70%
- 每个 API 端点至少一个测试
- 关键业务流程（编号生成、状态流转、权限）必须有测试

## 八、Git规范

- 分支：main / develop / feature/*
- 提交信息：`feat: xxx` / `fix: xxx` / `docs: xxx`
- PR 必须通过测试才能合并

## 九、数据库设计原则

- 完全自建，不依赖 Teable
- 独立 PostgreSQL 数据库（`baochen_mgmt`）
- 独立 schema，与 Teable 数据隔离
- 用户认证自建（JWT），不复用 Teable 用户体系

---

*本宪法由小诺编写，爸爸批准后生效。未经爸爸许可不可修改。*
