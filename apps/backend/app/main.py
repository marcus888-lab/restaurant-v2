from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import connect_db, disconnect_db
from app.core.config import settings
from app.api.v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Coffee Shop API...")
    await connect_db()
    yield
    # Shutdown
    print("Shutting down Coffee Shop API...")
    await disconnect_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Coffee Shop Application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Coffee Shop API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "coffee-shop-api"}

# Include API routes
app.include_router(api_router)