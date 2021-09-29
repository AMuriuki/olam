"""empty message

Revision ID: d07278b20e64
Revises: 0f31852cbd17
Create Date: 2021-09-29 13:47:21.224091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07278b20e64'
down_revision = '0f31852cbd17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.add_column(sa.Column('street', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('street2', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('county_id', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('country_id', sa.String(length=120), nullable=True))
        batch_op.create_index(batch_op.f('ix_partner_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_partner_country_id'), ['country_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_partner_county_id'), ['county_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_partner_street'), ['street'], unique=False)
        batch_op.create_index(batch_op.f('ix_partner_street2'), ['street2'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_partner_street2'))
        batch_op.drop_index(batch_op.f('ix_partner_street'))
        batch_op.drop_index(batch_op.f('ix_partner_county_id'))
        batch_op.drop_index(batch_op.f('ix_partner_country_id'))
        batch_op.drop_index(batch_op.f('ix_partner_city'))
        batch_op.drop_column('country_id')
        batch_op.drop_column('county_id')
        batch_op.drop_column('city')
        batch_op.drop_column('street2')
        batch_op.drop_column('street')

    # ### end Alembic commands ###
