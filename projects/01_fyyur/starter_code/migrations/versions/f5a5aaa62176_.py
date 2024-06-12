"""Adding columns to venue table

Revision ID: f5a5aaa62176
Revises: 8cd66693bce7
Create Date: 2024-06-12 08:40:25.545457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a5aaa62176'
down_revision = '8cd66693bce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('seeking_talent', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('seeking_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('website', sa.String(length=120), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.drop_column('website')
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_talent')
        batch_op.drop_column('genres')

    # ### end Alembic commands ###