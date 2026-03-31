# 宝宸专利管理系统 - 功能规格 v0.01

> 本文件定义所有功能需求，Claude Code 按此实现。

---

## 一、业务规则

### 1.1 编号规则
- 格式：`BCZL + 年月 + 类型 + 流水号`
- 类型：发明(1)/实用新型(2)/外观设计(3)
- 示例：`BCZL2026031001`
- **编号可修改**：普通用户可修改1次，项目所有人（徐健）可修改多次

### 1.2 案件流程
```
客户咨询 → 报价 → 客户确认 → 签合同 → 收到交底书/委托书
    → 撰写申请文件 → 四重质检 → 定稿 → 客户确认定稿
    → 递交（定稿后2个工作日内）→ 受理通知 → 审查
    → OA①（可能多次）→ 答复① → OA② → 答复② → ... → 授权/驳回 → 证书归档
```

### 1.3 费用规则
- 费用类型：**官费**和**代理费**（暂定）
- 允许对费用进行备注
- 中止规则：咨询1个月未签约 / 未付款15个工作日

### 1.4 期限管理
- **3级预警**（不是5级）：
  - 一级：到期前15天
  - 二级：到期前7天
  - 三级：到期前3天（升级通知爸爸）
- 无电话提醒

### 1.5 文件管理
- 文件夹命名：`客户简称-编号`
- 普通文件命名：用户指定或AI建议
- 官文命名：`官文名称-客户简称-专利号-绝限日期`
- 用户给文件 → AI识别 → 自动复制到对应文件夹 → 登记到documents表

### 1.6 合同管理
- 统一用一套合同，不区分瑞宸版/宝宸版

### 1.7 AI识别流程
- **任意用户**可通过对话要求AI识别文件
- AI识别后写入待确认队列
- **发起识别的用户**在Web页面查看/补充/编辑/确认

---

## 二、数据库表设计

### 2.1 clients（客户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| name | VARCHAR(200) NOT NULL | 客户名称 |
| short_name | VARCHAR(100) | 客户简称 |
| contact_person | VARCHAR(100) | 联系人 |
| phone | VARCHAR(50) | |
| email | VARCHAR(200) | |
| address | TEXT | |
| type | VARCHAR(20) DEFAULT '企业' | 企业/个人 |
| credit_code | VARCHAR(50) | 统一社会信用代码 |
| fee_reduction | BOOLEAN DEFAULT FALSE | 是否费减 |
| notes | TEXT | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### 2.2 cases（案件总表 - 主表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_number | VARCHAR(50) UNIQUE NOT NULL | BCZL2026031001 |
| entity | VARCHAR(20) DEFAULT '宝宸' | 宝宸/瑞宸 |
| client_id | FK → clients | |
| title | VARCHAR(500) NOT NULL | 发明名称 |
| patent_type | VARCHAR(20) NOT NULL | 发明/实用新型/外观设计 |
| application_number | VARCHAR(50) | 申请号 |
| filing_date | DATE | 申请日 |
| publication_number | VARCHAR(50) | 公开号 |
| grant_number | VARCHAR(50) | 授权公告号 |
| grant_date | DATE | 授权日 |
| applicant | TEXT | 申请人 |
| inventor | TEXT | 发明人 |
| agent_id | FK → users | 代理师 |
| assistant_id | FK → users | 协办人 |
| examiner | VARCHAR(100) | 审查员 |
| status | VARCHAR(50) DEFAULT '新案' | 状态枚举 |
| current_stage | VARCHAR(50) | 当前节点 |
| ipc_codes | VARCHAR(200) | IPC分类号 |
| tech_field | VARCHAR(100) | 技术领域 |
| priority_date | DATE | 优先权日 |
| nearest_deadline | DATE | 最近期限 |
| deadline_level | INTEGER DEFAULT 0 | 预警级别 0-3 |
| quotation_amount | DECIMAL(10,2) | 报价金额 |
| is_contract_signed | BOOLEAN DEFAULT FALSE | |
| notes | TEXT | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**状态枚举**：新案 → 撰写中 → 待质检 → 已定稿 → 待递交 → 已递交/在审 → 答复OA → 授权 → 驳回 → 放弃 → 结案归档

### 2.3 fees（费用表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| client_id | FK → clients | |
| fee_type | VARCHAR(100) NOT NULL | 官费/代理费 |
| amount | DECIMAL(10,2) NOT NULL | |
| fee_date | DATE | 应缴日期 |
| paid_date | DATE | 实缴日期 |
| status | VARCHAR(20) DEFAULT '未缴' | 未缴/已缴/减免/待确认 |
| fee_reduction | BOOLEAN DEFAULT FALSE | 是否费减 |
| receipt_number | VARCHAR(100) | 票据号 |
| invoice_number | VARCHAR(100) | 发票号 |
| notes | TEXT | 备注 |
| created_at | TIMESTAMP | |

### 2.4 file_locations（文件位置表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| parent_id | FK → file_locations | 父目录 |
| path | TEXT NOT NULL | 完整路径 |
| folder_name | VARCHAR(500) NOT NULL | |
| level | INTEGER DEFAULT 0 | 层级 |
| is_case_root | BOOLEAN DEFAULT FALSE | 案件根目录 |
| created_at | TIMESTAMP | |

**标准文件夹树**：
```
客户简称-编号/
├── 01_委托书/
├── 02_交底书/
├── 03_申请文件/
│   ├── 草稿/
│   └── 定稿/
├── 04_官方来文/
├── 05_答复文件/
├── 06_授权证书/
├── 07_合同/
├── 08_费用/
└── 09_其他/
```

### 2.5 documents（文件表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| doc_type | VARCHAR(50) NOT NULL | 文件类型 |
| file_name | VARCHAR(500) NOT NULL | |
| file_path | TEXT NOT NULL | |
| location_id | FK → file_locations | |
| file_size | INTEGER | |
| version | INTEGER DEFAULT 1 | |
| description | TEXT | |
| ai_extracted | BOOLEAN DEFAULT FALSE | |
| ai_confidence | DECIMAL(5,2) | |
| uploaded_by | VARCHAR(50) | |
| created_at | TIMESTAMP | |

### 2.6 deadlines（期限表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| deadline_type | VARCHAR(50) NOT NULL | OA答复/年费/递交/其他 |
| deadline_date | DATE NOT NULL | |
| warning_level | INTEGER DEFAULT 0 | 0-3级 |
| is_completed | BOOLEAN DEFAULT FALSE | |
| completed_date | DATE | |
| reminded_at | TIMESTAMP | |
| description | TEXT | |
| created_at | TIMESTAMP | |

### 2.7 official_letters（官方来文表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| letter_type | VARCHAR(100) NOT NULL | 官文类型枚举 |
| received_date | DATE NOT NULL | |
| official_number | VARCHAR(100) | |
| deadline_date | DATE | |
| summary | TEXT | AI摘要 |
| document_id | FK → documents | |
| is_processed | BOOLEAN DEFAULT FALSE | |
| processed_date | DATE | |
| notes | TEXT | |
| created_at | TIMESTAMP | |

**官文类型枚举（38+1种）**：

申请阶段(6)：专利申请受理通知书、申请费缴纳通知书、费用减缴审批通知书、补正通知书、视为撤回通知书（初审）、办理手续补正通知书

公布阶段(1)：发明专利申请公布通知书

实审阶段(8)：实质审查请求缴费通知书、进入实质审查阶段通知书、第一次审查意见通知书、第二次审查意见通知书、第三次及以上审查意见通知书、审查意见通知书（通用）、会晤通知书、优先审查通知书

授权/驳回(4)：授予专利权通知书、办理登记手续通知书、驳回决定、视为撤回通知书（实审）

复审阶段(4)：复审请求受理通知书、复审请求补正通知书、复审决定书（撤销驳回）、复审决定书（维持驳回）

授权后/维持(4)：专利登记通知书、年费缴纳通知书、专利权终止通知书、专利权评价报告

期限/权利(5)：期限届满通知书、恢复权利通知书、权利丧失通知书、中止程序通知书、解除中止通知书

其他(6)：著录项目变更通知书、转让手续审批通知书、分案申请通知书、撤回专利申请声明审批通知书、更正通知书、提前公布声明审批通知书

兜底(1)：其他官方文件

### 2.8 case_timeline（时间线表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| case_id | FK → cases | |
| status | VARCHAR(50) NOT NULL | |
| event_type | VARCHAR(50) NOT NULL | |
| event_date | DATE NOT NULL | |
| description | TEXT | |
| operator | VARCHAR(100) | |
| created_at | TIMESTAMP | |

### 2.9 users（系统用户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| name | VARCHAR(100) NOT NULL | |
| role | VARCHAR(50) DEFAULT 'staff' | admin/agent/staff |
| entity | VARCHAR(20) DEFAULT '宝宸' | |
| agent_number | VARCHAR(50) | 代理师资格证号 |
| email | VARCHAR(200) UNIQUE | |
| phone | VARCHAR(50) | |
| password_hash | VARCHAR(200) NOT NULL | |
| is_active | BOOLEAN DEFAULT TRUE | |
| created_at | TIMESTAMP | |

### 2.10 tasks（任务表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL PK | |
| title | VARCHAR(500) NOT NULL | |
| description | TEXT | |
| client_id | FK → clients | 关联客户 |
| client_name | VARCHAR(200) | 冗余 |
| client_short_name | VARCHAR(100) | 冗余 |
| case_id | FK → cases | 关联案件 |
| case_number | VARCHAR(50) | 冗余 |
| application_number | VARCHAR(50) | 冗余 |
| task_type | VARCHAR(50) NOT NULL | 撰写/答复OA/客户沟通/内部事务/质检/归档/其他 |
| priority | VARCHAR(20) DEFAULT '中' | 紧急/高/中/低 |
| status | VARCHAR(20) DEFAULT '待开始' | 待开始/进行中/待审核/已完成/已取消 |
| assignee_id | FK → users | |
| assistant_id | FK → users | |
| start_date | DATE | |
| due_date | DATE | |
| completed_date | DATE | |
| progress | INTEGER DEFAULT 0 | 0-100 |
| notes | TEXT | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

## 三、API端点

### 案件 /api/v1/cases
- GET / — 列表（筛选/搜索/分页）
- GET /{id} — 详情（含关联数据）
- POST / — 新建（自动编号）
- PUT /{id} — 更新
- PATCH /{id}/status — 更新状态（自动记录时间线）

### 待确认 /api/v1/pending
- GET / — 待确认列表
- POST /{id}/confirm — 确认写入主表
- POST /{id}/reject — 驳回

### 客户 /api/v1/clients
- GET / | GET /{id} | POST / | PUT /{id}

### 费用 /api/v1/fees
- GET /cases/{id}/fees | POST /cases/{id}/fees | GET /pending | GET /statistics

### 文件 /api/v1/documents
- GET /cases/{id}/documents | POST /cases/{id}/documents | GET /{id}/download

### 期限 /api/v1/deadlines
- GET / | GET /upcoming | POST /cases/{id}/deadlines

### 官文 /api/v1/letters
- GET /cases/{id}/letters | POST /cases/{id}/letters

### 任务 /api/v1/tasks
- GET / | GET /{id} | POST / | PUT /{id} | PATCH /{id}/status

### 统计 /api/v1/stats
- GET /dashboard | GET /monthly | GET /agent

### AI /api/v1/ai
- POST /query — 自然语言查询
- POST /recognize — PDF识别
- POST /import-pdf — 批量识别导入

### 认证 /api/v1/auth
- POST /login | POST /register | GET /me

---

## 四、前端页面（Airtable风格）

### 4.1 界面要求
- **Airtable风格**：网格视图为主，支持表单视图、看板视图
- 左侧导航栏
- 顶部工具栏（搜索、筛选、排序、视图切换）
- 网格：可内联编辑、可调整列宽、可冻结列
- 右侧抽屉：点击行展开详情
- 移动端适配

### 4.2 页面清单
1. 登录页
2. 仪表盘（总览+3级预警+待确认队列入口）
3. 待确认队列（AI识别结果，置信度标注）
4. 案件列表（网格视图，Airtable风格）
5. 案件详情（右侧抽屉或全页，含时间线/文件/费用/期限/官文Tab）
6. 案件编辑/新建（表单视图或模态框）
7. 客户列表
8. 客户详情
9. 费用管理
10. 文件管理
11. 期限日历
12. 官方来文
13. 任务列表（看板视图可选）
14. 统计报表

---

## 五、角色权限

| 操作 | admin（徐健） | operator（孙艳玲等） | readonly |
|------|--------------|---------------------|----------|
| 案件CRUD | ✅ | ✅ | 只读 |
| 编号修改 | ✅ 多次 | ✅ 1次 | ❌ |
| AI识别 | ✅ | ✅ | ❌ |
| 待确认编辑 | ✅ | ✅（自己发起的） | ❌ |
| 费用管理 | ✅ | ✅ | 只读 |
| 用户管理 | ✅ | ❌ | ❌ |
| 系统配置 | ✅ | ❌ | ❌ |
| 数据导出 | ✅ | ✅ | ✅ |
| 删除案件 | ✅ | ❌ | ❌ |

---

*本规格由小诺编写，爸爸批准后生效。*
