"""empty message

Revision ID: deb7ebd925b5
Revises: 93685df693ed
Create Date: 2021-10-02 20:44:36.393445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deb7ebd925b5'
down_revision = '93685df693ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expected_revenue', sa.Numeric(precision=10, scale=2), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.drop_column('expected_revenue')

    # ### end Alembic commands ###
