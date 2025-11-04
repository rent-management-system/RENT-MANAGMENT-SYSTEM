from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

from .routers import auth, users, admin
from .db.seed import seed_admin
from .db.session import get_db
from .utils.cleanup import cleanup_expired_refresh_tokens
from .core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed admin user
    async with get_db() as db:
        await seed_admin(db)
        break  # only need first session

    # Setup scheduler in EAT timezone
    eat_timezone = pytz.timezone('Africa/Addis_Ababa')
    scheduler = AsyncIOScheduler(timezone=eat_timezone)
    scheduler.add_job(
        cleanup_expired_refresh_tokens,
        'cron',
        hour=settings.CLEANUP_SCHEDULE_HOUR,  # e.g., 0 for midnight
        minute=0,
        id='refresh_token_cleanup_job'
    )
    scheduler.start()
    print("Scheduler started for refresh token cleanup.")

    yield

    # Shutdown scheduler
    scheduler.shutdown()
    print("Scheduler shut down.")

# Initialize FastAPI app
app = FastAPI(
    title="User Management Microservice",
    description="Manages users, authentication, and authorization.",
    version="1.0.0",
    lifespan=lifespan
)

# ====== CORS Middleware (allow all origins for testing) ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- allows any domain and path
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Health check endpoint ======
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# ====== Include Routers ======
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
