"""empty message

Revision ID: 0faf79e55412
Revises: 8f55a2f7e9f5
Create Date: 2021-09-28 11:38:23.712184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0faf79e55412'
down_revision = '8f55a2f7e9f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_name', sa.String(length=120), nullable=True))
        batch_op.create_index(batch_op.f('ix_partner_company_name'), ['company_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_partner_company_name'))
        batch_op.drop_column('company_name')

    # ### end Alembic commands ###
