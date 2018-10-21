"""grocery table

Revision ID: d8e4913bf112
Revises: 6f6cbe63a438
Create Date: 2018-10-19 22:32:05.869927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8e4913bf112'
down_revision = '6f6cbe63a438'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grocery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('items', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grocery_timestamp'), 'grocery', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_grocery_timestamp'), table_name='grocery')
    op.drop_table('grocery')
    # ### end Alembic commands ###
