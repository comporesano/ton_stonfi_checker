"""Refactored amount

Revision ID: e6ca98821d45
Revises: 7dde1ea790cf
Create Date: 2024-08-28 22:34:18.335137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6ca98821d45'
down_revision: Union[str, None] = '7dde1ea790cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'amount',
               existing_type=sa.NUMERIC(precision=10, scale=5),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'amount',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=10, scale=5),
               existing_nullable=True)
    # ### end Alembic commands ###
