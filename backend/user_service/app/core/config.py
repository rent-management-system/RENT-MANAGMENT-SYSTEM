from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, AnyUrl, validator

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT Settings
    JWT_SECRET: SecretStr                     # considered sensitive
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    RESET_TOKEN_EXPIRE_MINUTES: int = 15

    # Backwards-compat alias
    @property
    def secret_key(self) -> str:
        """Return JWT secret as plain string for libraries like python-jose"""
        return self.JWT_SECRET.get_secret_value()

    # Default Admin
    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    DEFAULT_ADMIN_EMAIL_2: str | None = None
    DEFAULT_ADMIN_PASSWORD_2: str | None = None

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # AES Encryption (sensitive)
    AES_SECRET_KEY: SecretStr

    # Supabase
    SUPABASE_URL: AnyUrl
    SUPABASE_SERVICE_ROLE_KEY: SecretStr

    # SMTP (Email)
    SMTP_USER: str
    SMTP_PASS: SecretStr
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    FRONTEND_URL: str

    # Cleanup Job
    CLEANUP_SCHEDULE_HOUR: int = 0

    # allow reading .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Validators
    @validator("SUPABASE_URL", pre=True)
    def strip_newlines_from_supabase_url(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if "\n" in v:
                raise ValueError(
                    "SUPABASE_URL contains newline(s). "
                    "Make sure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are separate environment variables."
                )
        return v

    @validator("SMTP_PORT", pre=True)
    def smtp_port_must_be_int(cls, v):
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

# Initialize settings
settings = Settings()
