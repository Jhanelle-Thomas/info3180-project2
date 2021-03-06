"""empty message

Revision ID: a34d21d40658
Revises: 2a0e5ccdb26a
Create Date: 2017-04-28 21:41:41.522849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a34d21d40658'
down_revision = '2a0e5ccdb26a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('email', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'email')
    # ### end Alembic commands ###
