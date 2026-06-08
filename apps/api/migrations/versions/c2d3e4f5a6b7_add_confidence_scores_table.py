"""add confidence_scores table

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-06-08 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'c2d3e4f5a6b7'
down_revision: Union[str, None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'confidence_scores',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column(
            'confidence_level',
            sa.Enum('low', 'medium', 'high', 'very_high', name='confidencelevel'),
            nullable=False,
        ),
        sa.Column('confidence_value', sa.Float(), nullable=False),
        sa.Column('approved_traceability_ratio', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('approved_requirements_ratio', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('approved_evidence_ratio', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('ai_only_decisions_ratio', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('open_gaps_ratio', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('calculated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_confidence_scores_project_id'), 'confidence_scores', ['project_id'], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_confidence_scores_project_id'), table_name='confidence_scores')
    op.drop_table('confidence_scores')
    op.execute("DROP TYPE IF EXISTS confidencelevel")
