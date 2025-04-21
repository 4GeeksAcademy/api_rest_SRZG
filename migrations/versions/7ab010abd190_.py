"""empty message

Revision ID: 7ab010abd190
Revises: 8eb108ae1f73
Create Date: 2025-04-21 14:10:11.658029

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = '7ab010abd190'
down_revision = '8eb108ae1f73'
branch_labels = None
depends_on = None


favorite_type_enum = pg.ENUM(
    'people', 'planets', 'vehicles', name='favorite_types')


def upgrade():
    favorite_type_enum.create(op.get_bind())
    op.add_column('favorites', sa.Column(
        'type', favorite_type_enum, nullable=False))


def downgrade():
    op.drop_column('favorites', 'type')
    favorite_type_enum.drop(op.get_bind())
