"""empty message

Revision ID: 13509f748958
Revises: 
Create Date: 2022-02-21 16:37:52.134036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13509f748958'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Test',

    )
    # ### end Alembic commands ###
