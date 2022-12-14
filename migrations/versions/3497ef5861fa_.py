"""empty message

Revision ID: 3497ef5861fa
Revises: 1f86733440a1
Create Date: 2022-08-14 00:43:00.626010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3497ef5861fa'
down_revision = '1f86733440a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_customer', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_column('is_customer')

    # ### end Alembic commands ###
