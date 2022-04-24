"""merging two heads

Revision ID: c75754f965ee
Revises: 086d48b697aa, a16401a2d3dd
Create Date: 2022-04-21 18:15:47.559656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c75754f965ee'
down_revision = ('086d48b697aa', 'a16401a2d3dd')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
