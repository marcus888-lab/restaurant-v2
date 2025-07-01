"""
Database connection and Prisma client setup.
"""
import os
from typing import Optional
from prisma import Prisma
from contextlib import asynccontextmanager

# Global Prisma client instance
prisma_client: Optional[Prisma] = None


def get_prisma_client() -> Prisma:
    """
    Get the global Prisma client instance.
    
    Returns:
        Prisma: The Prisma client instance
    """
    global prisma_client
    if prisma_client is None:
        prisma_client = Prisma()
    return prisma_client


async def connect_db():
    """
    Connect to the database using Prisma client.
    """
    client = get_prisma_client()
    if not client.is_connected():
        await client.connect()
        print("✅ Database connected successfully")


async def disconnect_db():
    """
    Disconnect from the database.
    """
    client = get_prisma_client()
    if client.is_connected():
        await client.disconnect()
        print("🔌 Database disconnected")


@asynccontextmanager
async def get_db():
    """
    Async context manager for database operations.
    Ensures proper connection handling.
    
    Yields:
        Prisma: Connected Prisma client
    """
    client = get_prisma_client()
    try:
        if not client.is_connected():
            await client.connect()
        yield client
    finally:
        # Don't disconnect here as we want to keep the connection pooled
        pass


# Dependency for FastAPI routes
async def get_db_dependency() -> Prisma:
    """
    FastAPI dependency to get database connection.
    
    Returns:
        Prisma: Connected Prisma client
    """
    client = get_prisma_client()
    if not client.is_connected():
        await client.connect()
    return client