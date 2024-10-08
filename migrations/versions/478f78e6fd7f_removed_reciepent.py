"""Removed reciepent

Revision ID: 478f78e6fd7f
Revises: 6f2346ddc319
Create Date: 2024-08-28 21:46:03.014477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '478f78e6fd7f'
down_revision: Union[str, None] = '6f2346ddc319'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('tx_hash', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'transaction', ['tx_hash'])
    op.drop_column('transaction', 'recipient')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('recipient', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transaction', type_='unique')
    op.drop_column('transaction', 'tx_hash')
    # ### end Alembic commands ###
