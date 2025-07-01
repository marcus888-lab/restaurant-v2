from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Coffee Shop API...")
    yield
    # Shutdown
    print("Shutting down Coffee Shop API...")

app = FastAPI(
    title="Coffee Shop API",
    description="Backend API for Coffee Shop Application",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:5175").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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