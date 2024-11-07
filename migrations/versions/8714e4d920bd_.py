"""empty message

Revision ID: 8714e4d920bd
Revises: 
Create Date: 2024-10-24 16:28:11.942070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8714e4d920bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crops',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('environmentStatus',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('humidity', sa.Float(), nullable=False),
    sa.Column('solidHumidity', sa.Float(), nullable=False),
    sa.Column('illuminance', sa.Float(), nullable=False),
    sa.Column('co2Concentration', sa.Float(), nullable=False),
    sa.Column('recorded_at', sa.DateTime(), nullable=False),
    sa.Column('crop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('environmentStatus')
    op.drop_table('crops')
    # ### end Alembic commands ###