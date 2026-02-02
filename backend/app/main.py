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

# Global exception handler for better error reporting
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# CORS middleware - allow all origins in development
cors_origins = settings.CORS_ORIGINS
logger.info(f"CORS origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
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
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/debug")
def debug_info():
    """Debug endpoint to check configuration."""
    from sqlalchemy import text
    from app.db.session import SessionLocal
    
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
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "running",
        "database": db_status,
        "tables": tables,
        "cors_origins": settings.CORS_ORIGINS,
        "debug_mode": settings.DEBUG,
    }
