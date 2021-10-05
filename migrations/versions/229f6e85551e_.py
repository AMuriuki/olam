"""empty message

Revision ID: 229f6e85551e
Revises: b7ebf1e8e077
Create Date: 2021-10-05 12:57:59.875962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229f6e85551e'
down_revision = 'b7ebf1e8e077'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_index('ix_partner_email')
        batch_op.create_index(batch_op.f('ix_partner_email'), ['email'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_partner_email'))
        batch_op.create_index('ix_partner_email', ['email'], unique=False)

    # ### end Alembic commands ###
