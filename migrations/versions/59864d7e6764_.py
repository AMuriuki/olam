"""empty message

Revision ID: 59864d7e6764
Revises: f1111f0feba7
Create Date: 2022-05-13 10:26:57.411374

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '59864d7e6764'
down_revision = 'f1111f0feba7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('tax_rate')

    with op.batch_alter_table('product_attribute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('index', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(batch_op.f('uq_product_attribute_index'), ['index'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_attribute', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_product_attribute_index'), type_='unique')
        batch_op.drop_column('index')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tax_rate', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))

    # ### end Alembic commands ###