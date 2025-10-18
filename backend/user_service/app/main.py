from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.routers import auth, users, admin # Will be created later

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

# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
