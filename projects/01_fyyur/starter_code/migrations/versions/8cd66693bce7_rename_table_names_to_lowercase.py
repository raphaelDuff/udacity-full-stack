"""rename table names to lowercase

Revision ID: 8cd66693bce7
Revises: 5a44f5ea2b42
Create Date: 2024-06-11 18:19:14.117267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cd66693bce7'
down_revision = '5a44f5ea2b42'
branch_labels = None
depends_on = None


def upgrade():
    # Rename table users to customers
    op.rename_table('Venue', 'venue')
    op.rename_table('Artist', 'artist')

def downgrade():
    # Rename table customers back to users
    op.rename_table('venue', 'Venue')
    op.rename_table('artist', 'Artist')
