from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz

from .routers import auth, users, admin
from .db.seed import seed_admin
from .db.session import get_db
from .utils.cleanup import cleanup_expired_refresh_tokens
from .core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async for db in get_db():
        await seed_admin(db)
        break

    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    # Schedule cleanup job daily at midnight EAT (UTC+3)
    # Convert current UTC time to EAT, then set to midnight, then convert back to UTC for scheduling
    eat_timezone = pytz.timezone('Africa/Addis_Ababa')
    now_utc = datetime.now(pytz.utc)
    now_eat = now_utc.astimezone(eat_timezone)
    
    # Set the desired cleanup hour in EAT (e.g., midnight is 0)
    cleanup_hour_eat = settings.CLEANUP_SCHEDULE_HOUR
    
    # Calculate the next run time in EAT, then convert to UTC for APScheduler
    next_run_eat = now_eat.replace(hour=cleanup_hour_eat, minute=0, second=0, microsecond=0)
    if next_run_eat <= now_eat:
        next_run_eat += timedelta(days=1) # Schedule for next day if time has passed today
    
    # Convert to UTC for APScheduler
    next_run_utc = next_run_eat.astimezone(pytz.utc)

    scheduler.add_job(
        cleanup_expired_refresh_tokens,
        'cron',
        hour=next_run_utc.hour,
        minute=next_run_utc.minute,
        id='refresh_token_cleanup_job'
    )
    scheduler.start()
    print("Scheduler started for refresh token cleanup.")

    yield

    # Shutdown
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(
    title="User Management Microservice",
    description="Manages users, authentication, and authorization.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # your Vite dev frontend
        "https://rental-user-management-frontend.vercel.app/",  # production frontend (if same domain serves UI)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
