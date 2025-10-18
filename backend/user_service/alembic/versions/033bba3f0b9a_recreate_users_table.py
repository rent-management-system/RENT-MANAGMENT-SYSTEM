"""Recreate users table

Revision ID: 033bba3f0b9a
Revises: f83322373a7e
Create Date: 2025-10-18 12:36:31.748167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '033bba3f0b9a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('properties') # Drop properties table first
    op.drop_table('users')

    op.execute("DROP TYPE IF EXISTS userrole;")
    op.execute("DROP TYPE IF EXISTS language;")
    op.execute("DROP TYPE IF EXISTS currency;")

    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'OWNER', 'TENANT', 'BROKER', name='userrole'), nullable=False),
        sa.Column('phone_number', sa.LargeBinary(), nullable=True),
        sa.Column('preferred_language', sa.Enum('EN', 'AM', 'OM', name='language'), nullable=True),
        sa.Column('preferred_currency', sa.Enum('ETB', 'USD', name='currency'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('password_changed', sa.Boolean(), server_default=sa.text('false'), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS userrole;")
    op.execute("DROP TYPE IF EXISTS language;")
    op.execute("DROP TYPE IF EXISTS currency;")
    # We are not recreating the original table in the downgrade, as it was in an inconsistent state.
    pass
