"""empty message

Revision ID: 46a553aadb67
Revises: 256ff5f1c271
Create Date: 2021-10-06 15:03:00.419251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46a553aadb67'
down_revision = '256ff5f1c271'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.add_column(sa.Column('partner_currency', sa.String(length=10), nullable=True))
        batch_op.create_index(batch_op.f('ix_lead_partner_currency'), ['partner_currency'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lead_partner_currency'))
        batch_op.drop_column('partner_currency')

    # ### end Alembic commands ###
