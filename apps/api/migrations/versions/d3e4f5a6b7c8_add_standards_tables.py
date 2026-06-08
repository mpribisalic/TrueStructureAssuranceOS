"""add standards, standard_clauses, requirement_standard_links tables

Revision ID: d3e4f5a6b7c8
Revises: c2d3e4f5a6b7
Create Date: 2026-06-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'd3e4f5a6b7c8'
down_revision: Union[str, None] = 'c2d3e4f5a6b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'standards',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column(
            'standard_type',
            sa.Enum(
                'nato_stanag', 'do_178c', 'do_254', 'iso_26262',
                'iec_61508', 'iec_62304', 'en_50128', 'custom',
                name='standardtype',
            ),
            nullable=False,
        ),
        sa.Column('version', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'standard_clauses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('standard_id', sa.UUID(), nullable=False),
        sa.Column('clause_id', sa.String(100), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['standard_id'], ['standards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_standard_clauses_standard_id'), 'standard_clauses', ['standard_id'], unique=False
    )

    op.create_table(
        'requirement_standard_links',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('requirement_id', sa.UUID(), nullable=False),
        sa.Column('standard_clause_id', sa.UUID(), nullable=False),
        sa.Column('coverage_status', sa.String(50), nullable=False, server_default='partial'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['standard_clause_id'], ['standard_clauses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_requirement_standard_links_requirement_id'),
        'requirement_standard_links', ['requirement_id'], unique=False
    )
    op.create_index(
        op.f('ix_requirement_standard_links_standard_clause_id'),
        'requirement_standard_links', ['standard_clause_id'], unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_requirement_standard_links_standard_clause_id'),
        table_name='requirement_standard_links'
    )
    op.drop_index(
        op.f('ix_requirement_standard_links_requirement_id'),
        table_name='requirement_standard_links'
    )
    op.drop_table('requirement_standard_links')
    op.drop_index(op.f('ix_standard_clauses_standard_id'), table_name='standard_clauses')
    op.drop_table('standard_clauses')
    op.drop_table('standards')
    op.execute("DROP TYPE IF EXISTS standardtype")
