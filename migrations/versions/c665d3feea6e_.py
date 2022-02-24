"""empty message

Revision ID: c665d3feea6e
Revises: 57aa9994ff31
Create Date: 2022-02-17 13:59:40.066904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c665d3feea6e'
down_revision = '57aa9994ff31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('module_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_model_module_id_module'), 'module', ['module_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('model', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_model_module_id_module'), type_='foreignkey')
        batch_op.drop_column('module_id')

    # ### end Alembic commands ###