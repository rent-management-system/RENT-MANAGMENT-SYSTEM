from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import secrets
from supabase import create_client

# Local imports
from app.routers import auth, users, admin
from app.db.seed import seed_admin
from app.db.session import get_db
from app.utils.cleanup import cleanup_expired_refresh_tokens
from app.utils.send_email import send_reset_email
from app.core.config import settings

# Initialize Supabase
url = "https://spdwbxirjclmafdwzkvu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNwZHdieGlyamNsbWFmZHd6a3Z1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTE0OTk1NywiZXhwIjoyMDc2NzI1OTU3fQ.dAozqRHJeqrVlpBXdjwATLEH6R8BqfOR0mAeS1oJxR8"
supabase = create_client(url, key)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Seeding admin user...")
    async for db in get_db():
        await seed_admin(db)
    print("Admin user seeding complete.")

    eat_timezone = pytz.timezone('Africa/Addis_Ababa')
    scheduler = AsyncIOScheduler(timezone=eat_timezone)
    scheduler.add_job(
        cleanup_expired_refresh_tokens,
        'cron',
        hour=settings.CLEANUP_SCHEDULE_HOUR,
        minute=0,
        id='refresh_token_cleanup_job'
    )
    scheduler.start()
    print("Scheduler started for refresh token cleanup.")
    yield
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(
    title="User Management Microservice",
    description="Manages users, authentication, and authorization.",
    version="1.0.0",
    lifespan=lifespan
)

# ====== CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Routes ======

@app.get("/")
def root():
    return {"message": "User service is running 🚀"}

@app.options("/forgot-password")
async def preflight():
    return JSONResponse(content={"message": "CORS preflight OK"})

@app.post("/forgot-password")
async def forgot_password(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON"})

    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = supabase.table("users").select("*").eq("email", email).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.data[0]["id"]
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    reset_link = f"http://localhost:5174/reset-password?token={token}"

    supabase.table("password_resets").insert({
        "user_id": user_id,
        "email": email,
        "token": token,
        "expires_at": expires_at.isoformat(),
    }).execute()

    try:
        send_reset_email(email, reset_link)
        return {"message": "Reset link sent successfully"}
    except Exception as e:
        print("❌ Failed to send email:", e)
        raise HTTPException(status_code=500, detail="Failed to send reset email")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# ====== Include Routers ======
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
