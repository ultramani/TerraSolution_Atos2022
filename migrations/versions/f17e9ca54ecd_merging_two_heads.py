"""merging two heads

Revision ID: f17e9ca54ecd
Revises: 119f639af64b, 8def2e35be63
Create Date: 2022-04-17 22:52:35.257363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f17e9ca54ecd'
down_revision = ('119f639af64b', '8def2e35be63')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
