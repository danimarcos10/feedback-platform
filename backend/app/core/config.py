from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Feedback Platform"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/feedback_db"
    
    # JWT Authentication
    # IMPORTANT: Set SECRET_KEY via environment variable in production!
    # The default is for local development only and is NOT secure.
    SECRET_KEY: str = "dev-only-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Demo/Seed Data
    ADMIN_EMAIL: str = "admin@demo.com"
    ADMIN_PASSWORD: str = "admin1234"
    DEMO_USER_EMAIL: str = "user@demo.com"
    DEMO_USER_PASSWORD: str = "user1234"
    SEED_DEMO_DATA: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
