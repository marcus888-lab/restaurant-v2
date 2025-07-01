from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prisma.errors import PrismaError
from contextlib import asynccontextmanager
import logging

from app.core.database import connect_db, disconnect_db
from app.core.config import settings
from app.core.middleware import RequestIDMiddleware, LoggingMiddleware, ErrorHandlingMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    prisma_exception_handler,
    general_exception_handler
)
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Coffee Shop API...")
    await connect_db()
    yield
    # Shutdown
    logger.info("Shutting down Coffee Shop API...")
    await disconnect_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Coffee Shop Application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add middleware in reverse order (last added is executed first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Add exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(PrismaError, prisma_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to Coffee Shop API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    try:
        from app.core.database import get_prisma_client
        db = get_prisma_client()
        await db.user.count()
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": "coffee-shop-api",
        "database": db_status
    }

# Include API routes
app.include_router(api_router)