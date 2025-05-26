import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from config import settings
from models.user import User
from models.course import Course

load_dotenv()

async def init_db():
    """Initialize database connection and models."""
    # Validate configuration
    settings.validate()
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGO_URI)
    
    # Initialize Beanie with the document models
    await init_beanie(
        database=client[settings.DB_NAME],
        document_models=[User, Course]
    )
    
    print(f"Connected to MongoDB database: {settings.DB_NAME}")
