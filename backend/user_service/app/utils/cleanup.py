import asyncio
from datetime import datetime, timedelta
import pytz

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..db.session import get_db
from ..models.user import RefreshToken
from .retry import async_retry

# Define the EAT timezone
EAT = pytz.timezone('Africa/Addis_Ababa')

@async_retry(tries=3, delay=2, backoff=2)
async def cleanup_expired_refresh_tokens():
    print("Starting cleanup of expired refresh tokens...")
    async for db in get_db():
        try:
            # Calculate the expiration threshold (7 days ago from now in EAT)
            # Convert current UTC time to EAT, then subtract 7 days
            now_utc = datetime.now(pytz.utc)
            now_eat = now_utc.astimezone(EAT)
            expiration_threshold = now_eat - timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

            # Delete tokens where expires_at is older than the threshold
            result = await db.execute(
                delete(RefreshToken).where(RefreshToken.expires_at < expiration_threshold)
            )
            deleted_count = result.rowcount
            await db.commit()
            print(f"Cleanup complete: Deleted {deleted_count} expired refresh tokens.")
        except Exception as e:
            print(f"Error during refresh token cleanup: {e}")
            await db.rollback()
            raise # Re-raise to trigger retry
