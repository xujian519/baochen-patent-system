"""Initial tables - 创建所有基础表

Revision ID: 001
Revises:
Create Date: 2026-03-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建所有基础表"""

    # 1. 创建 users 表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, comment='姓名'),
        sa.Column('role', sa.String(50), server_default='staff', comment='角色: admin/agent/staff'),
        sa.Column('entity', sa.String(20), server_default='宝宸', comment='主体: 宝宸/瑞宸'),
        sa.Column('agent_number', sa.String(50), comment='代理师资格证号'),
        sa.Column('email', sa.String(200), unique=True, comment='邮箱'),
        sa.Column('phone', sa.String(50), comment='电话'),
        sa.Column('password_hash', sa.String(200), nullable=False, comment='密码哈希'),
        sa.Column('is_active', sa.Boolean(), server_default='true', comment='是否激活'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'])

    # 2. 创建 clients 表
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False, comment='客户名称'),
        sa.Column('short_name', sa.String(100), comment='客户简称'),
        sa.Column('contact_person', sa.String(100), comment='联系人'),
        sa.Column('phone', sa.String(50), comment='电话'),
        sa.Column('email', sa.String(200), comment='邮箱'),
        sa.Column('address', sa.Text(), comment='地址'),
        sa.Column('type', sa.String(20), server_default='企业', comment='类型: 企业/个人'),
        sa.Column('credit_code', sa.String(50), comment='统一社会信用代码'),
        sa.Column('fee_reduction', sa.Boolean(), server_default='false', comment='是否费减'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_clients_id', 'clients', ['id'])

    # 3. 创建 cases 表（主表）
    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_number', sa.String(50), unique=True, nullable=False, comment='案件编号'),
        sa.Column('entity', sa.String(20), server_default='宝宸', comment='主体'),
        sa.Column('client_id', sa.Integer(), comment='客户ID'),
        sa.Column('title', sa.String(500), nullable=False, comment='发明名称'),
        sa.Column('patent_type', sa.String(20), nullable=False, comment='专利类型'),
        sa.Column('application_number', sa.String(50), comment='申请号'),
        sa.Column('filing_date', sa.Date(), comment='申请日'),
        sa.Column('publication_number', sa.String(50), comment='公开号'),
        sa.Column('grant_number', sa.String(50), comment='授权公告号'),
        sa.Column('grant_date', sa.Date(), comment='授权日'),
        sa.Column('applicant', sa.Text(), comment='申请人'),
        sa.Column('inventor', sa.Text(), comment='发明人'),
        sa.Column('agent_id', sa.Integer(), comment='代理师ID'),
        sa.Column('assistant_id', sa.Integer(), comment='协办人ID'),
        sa.Column('examiner', sa.String(100), comment='审查员'),
        sa.Column('status', sa.String(50), server_default='新案', comment='状态'),
        sa.Column('current_stage', sa.String(50), comment='当前节点'),
        sa.Column('ipc_codes', sa.String(200), comment='IPC分类号'),
        sa.Column('tech_field', sa.String(100), comment='技术领域'),
        sa.Column('priority_date', sa.Date(), comment='优先权日'),
        sa.Column('nearest_deadline', sa.Date(), comment='最近期限'),
        sa.Column('deadline_level', sa.Integer(), server_default='0', comment='预警级别'),
        sa.Column('quotation_amount', sa.Numeric(10, 2), comment='报价金额'),
        sa.Column('is_contract_signed', sa.Boolean(), server_default='false', comment='是否签合同'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['agent_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['assistant_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cases_id', 'cases', ['id'])
    op.create_index('ix_cases_case_number', 'cases', ['case_number'])
    op.create_index('ix_cases_client_id', 'cases', ['client_id'])

    # 4. 创建 fees 表
    op.create_table(
        'fees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('client_id', sa.Integer(), comment='客户ID'),
        sa.Column('fee_type', sa.String(100), nullable=False, comment='费用类型'),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False, comment='金额'),
        sa.Column('fee_date', sa.Date(), comment='应缴日期'),
        sa.Column('paid_date', sa.Date(), comment='实缴日期'),
        sa.Column('status', sa.String(20), server_default='未缴', comment='状态'),
        sa.Column('fee_reduction', sa.Boolean(), server_default='false', comment='是否费减'),
        sa.Column('receipt_number', sa.String(100), comment='票据号'),
        sa.Column('invoice_number', sa.String(100), comment='发票号'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_fees_id', 'fees', ['id'])
    op.create_index('ix_fees_case_id', 'fees', ['case_id'])
    op.create_index('ix_fees_client_id', 'fees', ['client_id'])

    # 5. 创建 file_locations 表
    op.create_table(
        'file_locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('parent_id', sa.Integer(), comment='父目录ID'),
        sa.Column('path', sa.Text(), nullable=False, comment='完整路径'),
        sa.Column('folder_name', sa.String(500), nullable=False, comment='文件夹名称'),
        sa.Column('level', sa.Integer(), server_default='0', comment='层级深度'),
        sa.Column('is_case_root', sa.Boolean(), server_default='false', comment='是否为案件根目录'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['file_locations.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_file_locations_id', 'file_locations', ['id'])
    op.create_index('ix_file_locations_case_id', 'file_locations', ['case_id'])

    # 6. 创建 documents 表
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('doc_type', sa.String(50), nullable=False, comment='文件类型'),
        sa.Column('file_name', sa.String(500), nullable=False, comment='文件名'),
        sa.Column('file_path', sa.Text(), nullable=False, comment='文件路径'),
        sa.Column('location_id', sa.Integer(), comment='文件位置ID'),
        sa.Column('file_size', sa.Integer(), comment='文件大小'),
        sa.Column('version', sa.Integer(), server_default='1', comment='版本号'),
        sa.Column('description', sa.Text(), comment='描述'),
        sa.Column('ai_extracted', sa.Boolean(), server_default='false', comment='AI是否已提取'),
        sa.Column('ai_confidence', sa.Numeric(5, 2), comment='AI置信度'),
        sa.Column('uploaded_by', sa.String(50), comment='上传者'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['file_locations.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_id', 'documents', ['id'])
    op.create_index('ix_documents_case_id', 'documents', ['case_id'])

    # 7. 创建 deadlines 表
    op.create_table(
        'deadlines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('deadline_type', sa.String(50), nullable=False, comment='期限类型'),
        sa.Column('deadline_date', sa.Date(), nullable=False, comment='截止日期'),
        sa.Column('warning_level', sa.Integer(), server_default='0', comment='预警级别'),
        sa.Column('is_completed', sa.Boolean(), server_default='false', comment='是否已完成'),
        sa.Column('completed_date', sa.Date(), comment='完成日期'),
        sa.Column('reminded_at', sa.DateTime(), comment='最近提醒时间'),
        sa.Column('description', sa.Text(), comment='描述'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_deadlines_id', 'deadlines', ['id'])
    op.create_index('ix_deadlines_case_id', 'deadlines', ['case_id'])
    op.create_index('ix_deadlines_deadline_date', 'deadlines', ['deadline_date'])

    # 8. 创建 official_letters 表
    op.create_table(
        'official_letters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('letter_type', sa.String(100), nullable=False, comment='官文类型'),
        sa.Column('received_date', sa.Date(), nullable=False, comment='收到日期'),
        sa.Column('official_number', sa.String(100), comment='官文编号'),
        sa.Column('deadline_date', sa.Date(), comment='答复期限'),
        sa.Column('summary', sa.Text(), comment='AI摘要'),
        sa.Column('document_id', sa.Integer(), comment='关联文档ID'),
        sa.Column('is_processed', sa.Boolean(), server_default='false', comment='是否已处理'),
        sa.Column('processed_date', sa.Date(), comment='处理日期'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_official_letters_id', 'official_letters', ['id'])
    op.create_index('ix_official_letters_case_id', 'official_letters', ['case_id'])

    # 9. 创建 case_timeline 表
    op.create_table(
        'case_timeline',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('status', sa.String(50), nullable=False, comment='状态'),
        sa.Column('event_type', sa.String(50), nullable=False, comment='事件类型'),
        sa.Column('event_date', sa.Date(), nullable=False, comment='事件日期'),
        sa.Column('description', sa.Text(), comment='描述'),
        sa.Column('operator', sa.String(100), comment='操作人'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_case_timeline_id', 'case_timeline', ['id'])
    op.create_index('ix_case_timeline_case_id', 'case_timeline', ['case_id'])

    # 10. 创建 tasks 表
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(500), nullable=False, comment='任务标题'),
        sa.Column('description', sa.Text(), comment='任务描述'),
        sa.Column('client_id', sa.Integer(), comment='客户ID'),
        sa.Column('client_name', sa.String(200), comment='客户名称'),
        sa.Column('client_short_name', sa.String(100), comment='客户简称'),
        sa.Column('case_id', sa.Integer(), comment='案件ID'),
        sa.Column('case_number', sa.String(50), comment='案件编号'),
        sa.Column('application_number', sa.String(50), comment='申请号'),
        sa.Column('task_type', sa.String(50), nullable=False, comment='任务类型'),
        sa.Column('priority', sa.String(20), server_default='中', comment='优先级'),
        sa.Column('status', sa.String(20), server_default='待开始', comment='状态'),
        sa.Column('assignee_id', sa.Integer(), comment='负责人ID'),
        sa.Column('assistant_id', sa.Integer(), comment='协助人ID'),
        sa.Column('start_date', sa.Date(), comment='开始日期'),
        sa.Column('due_date', sa.Date(), comment='截止日期'),
        sa.Column('completed_date', sa.Date(), comment='完成日期'),
        sa.Column('progress', sa.Integer(), server_default='0', comment='进度'),
        sa.Column('notes', sa.Text(), comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['assistant_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'])
    op.create_index('ix_tasks_client_id', 'tasks', ['client_id'])
    op.create_index('ix_tasks_case_id', 'tasks', ['case_id'])


def downgrade() -> None:
    """回滚 - 删除所有表"""
    # 按照依赖关系逆序删除
    op.drop_table('tasks')
    op.drop_table('case_timeline')
    op.drop_table('official_letters')
    op.drop_table('deadlines')
    op.drop_table('documents')
    op.drop_table('file_locations')
    op.drop_table('fees')
    op.drop_table('cases')
    op.drop_table('clients')
    op.drop_table('users')
