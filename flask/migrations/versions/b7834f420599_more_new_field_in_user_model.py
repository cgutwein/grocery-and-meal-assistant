"""more new field in user model

Revision ID: b7834f420599
Revises: e67b85f9c1cd
Create Date: 2018-11-24 19:01:38.000312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7834f420599'
down_revision = 'e67b85f9c1cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('carb', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('complexity', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('cuisine', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('daily_cal', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('fat', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('gender', sa.String(length=1), nullable=True))
    op.add_column('user', sa.Column('goals', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('gym', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('protein', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('restrictions', sa.String(length=10), nullable=True))
    op.add_column('user', sa.Column('weight', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'weight')
    op.drop_column('user', 'restrictions')
    op.drop_column('user', 'protein')
    op.drop_column('user', 'height')
    op.drop_column('user', 'gym')
    op.drop_column('user', 'goals')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'fat')
    op.drop_column('user', 'daily_cal')
    op.drop_column('user', 'cuisine')
    op.drop_column('user', 'complexity')
    op.drop_column('user', 'carb')
    op.drop_column('user', 'age')
    # ### end Alembic commands ###
