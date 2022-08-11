"""empty message

Revision ID: c8e2b9548b19
Revises: e3249f44e38d
Create Date: 2022-08-11 23:29:20.424504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e2b9548b19'
down_revision = 'e3249f44e38d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color_badge', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.drop_column('color_badge')

    # ### end Alembic commands ###
