"""Cria Tabela de contas a pagar e receber

Revision ID: f4ca06f6c0a0
Revises: 
Create Date: 2025-07-27 08:46:00.692852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ca06f6c0a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'contas_a_pagar_e_receber',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('descricao', sa.String(length=30), nullable=True),
        sa.Column('valor', sa.Numeric(), nullable=True),
        sa.Column('tipo', sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('contas_a_pagar_e_receber')
