"""another new field

Revision ID: c17e4c1101de
Revises: b7834f420599
Create Date: 2018-11-24 21:57:07.208365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17e4c1101de'
down_revision = 'b7834f420599'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('scores_fn', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'scores_fn')
    # ### end Alembic commands ###
