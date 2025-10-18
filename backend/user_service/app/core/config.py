from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT Settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Default Admin
    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    DEFAULT_ADMIN_EMAIL_2: str | None = None # Optional second admin email
    DEFAULT_ADMIN_PASSWORD_2: str | None = None # Optional second admin password

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # AES Encryption
    AES_SECRET_KEY: str

    # Cleanup Job
    CLEANUP_SCHEDULE_HOUR: int = 0 # Midnight EAT (UTC+3)

    class Config:
        env_file = ".env"

settings = Settings()
