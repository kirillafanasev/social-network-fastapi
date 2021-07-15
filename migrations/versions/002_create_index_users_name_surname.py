"""create idx_users_name_surname index

Revision ID: 002
Revises: 001
Create Date: 2021-07-05 23:25:32.006984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        'idx_users_name_surname',
        'users',
        ['name', 'surname']
    )


def downgrade():
    op.drop_index('idx_users_name_surname', 'users')
