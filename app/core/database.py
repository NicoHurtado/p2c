import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
import logging
from .config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """MongoDB Atlas database manager with connection pooling"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.settings = get_settings()
    
    async def connect(self):
        """Establish connection to MongoDB Atlas"""
        try:
            self.client = AsyncIOMotorClient(
                self.settings.get_mongodb_url(),
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=20000
            )
            
            # Test connection
            await self.client.admin.command('ping')
            
            self.database = self.client[self.settings.database_name]
            
            # Create indexes for optimization
            await self._create_indexes()
            
            logger.info("Successfully connected to MongoDB Atlas")
            
        except ServerSelectionTimeoutError:
            logger.error("Failed to connect to MongoDB Atlas - Server selection timeout")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {str(e)}")
            raise
    
    async def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB Atlas")
    
    async def _create_indexes(self):
        """Create database indexes for optimal performance"""
        if self.database is None:
            return
            
        try:
            # Courses collection indexes
            courses_collection = self.database.courses
            await courses_collection.create_index("user_prompt")
            await courses_collection.create_index("user_level")
            await courses_collection.create_index("user_interests")
            await courses_collection.create_index("status")
            await courses_collection.create_index("created_at")
            await courses_collection.create_index([("user_prompt", "text"), ("metadata.title", "text")])
            
            # Audio resources collection indexes
            audio_collection = self.database.audio_resources
            await audio_collection.create_index("created_by")
            await audio_collection.create_index("created_at")
            await audio_collection.create_index("language")
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create some indexes: {str(e)}")
    
    def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database
    
    async def health_check(self) -> bool:
        """Check database health"""
        try:
            if self.client is None:
                return False
            await self.client.admin.command('ping')
            return True
        except Exception:
            return False


# Global database manager instance
db_manager = DatabaseManager()


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database instance"""
    return db_manager.get_database()


async def init_database():
    """Initialize database connection"""
    await db_manager.connect()


async def close_database():
    """Close database connection"""
    await db_manager.disconnect() 