from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, admin

app = FastAPI(
    title="User Management Microservice",
    description="Manages users, authentication, and authorization.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
from app.db.seed import seed_admin
from app.db.session import get_db

@app.on_event("startup")
async def on_startup():
    async for db in get_db():
        await seed_admin(db)
        break
