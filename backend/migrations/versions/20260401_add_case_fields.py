"""添加案件新字段：案件状态、专利权人、费减比例等

Revision ID: 20260401_add_case_fields
Revises: 20260331_initial_tables
Create Date: 2026-04-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260401_add_case_fields'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # 1. 重命名 status 为 stage（案件阶段）
    op.alter_column('cases', 'status', new_column_name='stage')

    # 2. 添加新字段
    op.add_column('cases', sa.Column('case_status', sa.String(20), server_default='进行中', comment='案件状态: 进行中/已结案/已终止/已暂停'))
    op.add_column('cases', sa.Column('patent_holder', sa.String(500), nullable=True, comment='专利权人'))
    op.add_column('cases', sa.Column('fee_reduction_ratio', sa.Integer, server_default='0', comment='费减比例: 0/70/85/100'))


def downgrade():
    # 1. 删除新字段
    op.drop_column('cases', 'fee_reduction_ratio')
    op.drop_column('cases', 'patent_holder')
    op.drop_column('cases', 'case_status')

    # 2. 重命名 stage 回 status
    op.alter_column('cases', 'stage', new_column_name='status')
