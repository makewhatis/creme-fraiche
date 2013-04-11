"""add status column to users table

Revision ID: 588808597661
Revises: None
Create Date: 2013-04-11 00:00:49.889877

"""

# revision identifiers, used by Alembic.
revision = '588808597661'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'users',
        sa.Users('status', sa.Boolean
    )

def downgrade():
    op.drop_column(
        'users',
        'status'
    )

