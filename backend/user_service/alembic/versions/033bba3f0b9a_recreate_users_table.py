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


from sqlalchemy import Index, ForeignKey
def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TABLE IF EXISTS properties CASCADE;") # Drop properties table first
    op.execute("DROP TABLE IF EXISTS refresh_tokens CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")

    op.execute("DROP TYPE IF EXISTS userrole CASCADE;")
    op.execute("DROP TYPE IF EXISTS language CASCADE;")
    op.execute("DROP TYPE IF EXISTS currency CASCADE;")

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
    op.create_table(
        'refresh_tokens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('user_id', UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    )
    op.create_index('idx_refresh_token_expires_at', 'refresh_tokens', ['expires_at'], unique=False)
    op.create_index('idx_refresh_token_user_id', 'refresh_tokens', ['user_id'], unique=False)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS userrole;")
    op.execute("DROP TYPE IF EXISTS language;")
    op.execute("DROP TYPE IF EXISTS currency;")
    # We are not recreating the original table in the downgrade, as it was in an inconsistent state.
    pass
