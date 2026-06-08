"""add mission_impacts table

Revision ID: b1c2d3e4f5a6
Revises: a8bef92d14b1
Create Date: 2026-06-08 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, None] = 'a8bef92d14b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'mission_impacts',
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('related_gap_id', sa.UUID(), nullable=True),
        sa.Column(
            'impact_category',
            sa.Enum('safety', 'cyber', 'mission', 'availability', 'reliability', 'compliance',
                    name='impactcategory'),
            nullable=False,
        ),
        sa.Column(
            'impact_level',
            sa.Enum('low', 'medium', 'high', 'critical', name='impactlevel'),
            nullable=False,
        ),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('operational_consequence', sa.Text(), nullable=False),
        sa.Column('mission_consequence', sa.Text(), nullable=False),
        sa.Column('readiness_delta', sa.Float(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['related_gap_id'], ['gaps.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_mission_impacts_project_id'), 'mission_impacts', ['project_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_mission_impacts_project_id'), table_name='mission_impacts')
    op.drop_table('mission_impacts')
    op.execute("DROP TYPE IF EXISTS impactcategory")
    op.execute("DROP TYPE IF EXISTS impactlevel")
