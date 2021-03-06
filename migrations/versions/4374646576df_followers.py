"""followers

Revision ID: 4374646576df
Revises: bda56eb411a6
Create Date: 2022-01-30 23:00:23.268785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4374646576df'
down_revision = 'bda56eb411a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
