import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.routes import (
    auth_router,
    users_router,
    feedback_router,
    admin_router,
    analytics_router,
    categories_router,
    tags_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="A comprehensive feedback platform with analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global exception handler - logs details but doesn't leak them to client
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full details for debugging (server-side only)
    logger.error(f"Unhandled error on {request.method} {request.url}: {exc}", exc_info=True)
    
    # Return generic message to client (don't leak internal details)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )

# CORS middleware
cors_origins = settings.CORS_ORIGINS or ["http://localhost:5173", "http://localhost", "http://localhost:80"]
logger.info(f"CORS origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(feedback_router)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(categories_router)
app.include_router(tags_router)


@app.on_event("startup")
async def startup_event():
    """Log startup information and test database connection."""
    from sqlalchemy import text
    from app.db.session import engine
    
    logger.info("=" * 50)
    logger.info("Feedback Platform API Starting...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Test database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection: OK")
    except Exception as e:
        logger.error(f"Database connection FAILED: {e}")
        logger.error("Make sure the database is running and migrations have been applied!")
        logger.info("=" * 50)
        return
    
    # Seed demo data if enabled
    if settings.SEED_DEMO_DATA:
        logger.info("SEED_DEMO_DATA is enabled, seeding demo data...")
        try:
            from app.seed import seed
            seed()
        except Exception as e:
            logger.error(f"Failed to seed demo data: {e}")
    
    logger.info("API Docs available at: /docs")
    logger.info("=" * 50)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Feedback Platform API", "status": "healthy"}


@app.get("/health")
def health_check():
    """Health check endpoint with database test."""
    from sqlalchemy import text
    from app.db.session import SessionLocal
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        # Don't leak internal error details
        return {"status": "unhealthy", "database": "disconnected"}


@app.get("/debug")
def debug_info():
    """Debug endpoint to check configuration (only available in DEBUG mode)."""
    from fastapi import HTTPException
    from sqlalchemy import text
    from app.db.session import SessionLocal
    
    # Only allow in debug mode to prevent information leakage
    if not settings.DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    
    db_status = "unknown"
    tables = []
    
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        # Check if tables exist
        result = db.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        ))
        tables = [row[0] for row in result.fetchall()]
        db.close()
        db_status = "connected"
    except Exception:
        db_status = "error"
    
    return {
        "status": "running",
        "database": db_status,
        "tables": tables,
        "cors_origins": settings.CORS_ORIGINS,
        "debug_mode": settings.DEBUG,
    }
