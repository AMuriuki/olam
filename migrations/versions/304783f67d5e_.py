"""empty message

Revision ID: 304783f67d5e
Revises: 34679c34afbc
Create Date: 2021-09-30 11:36:10.915736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304783f67d5e'
down_revision = '34679c34afbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('postal_code', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('postal_address', sa.String(length=120), nullable=True))
        batch_op.drop_index('ix_partner_street')
        batch_op.drop_index('ix_partner_street2')
        batch_op.create_index(batch_op.f('ix_partner_postal_address'), ['postal_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_partner_postal_code'), ['postal_code'], unique=False)
        batch_op.drop_column('street2')
        batch_op.drop_column('street')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('street', sa.VARCHAR(length=120), nullable=True))
        batch_op.add_column(sa.Column('street2', sa.VARCHAR(length=120), nullable=True))
        batch_op.drop_index(batch_op.f('ix_partner_postal_code'))
        batch_op.drop_index(batch_op.f('ix_partner_postal_address'))
        batch_op.create_index('ix_partner_street2', ['street2'], unique=False)
        batch_op.create_index('ix_partner_street', ['street'], unique=False)
        batch_op.drop_column('postal_address')
        batch_op.drop_column('postal_code')

    # ### end Alembic commands ###
