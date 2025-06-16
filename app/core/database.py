import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError, NetworkTimeout, AutoReconnect
import logging
from .config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """MongoDB Atlas database manager with connection pooling and robust error handling"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self.settings = get_settings()
    
    async def connect(self):
        """Establish connection to MongoDB Atlas with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to connect to MongoDB Atlas (attempt {attempt + 1}/{max_retries})")
                
                self.client = AsyncIOMotorClient(
                    self.settings.get_mongodb_url(),
                    maxPoolSize=50,
                    minPoolSize=5,
                    maxIdleTimeMS=60000,  # Increased from 30000
                    serverSelectionTimeoutMS=30000,  # Increased from 5000
                    connectTimeoutMS=20000,  # Increased from 10000
                    socketTimeoutMS=60000,  # Increased from 20000
                    heartbeatFrequencyMS=10000,  # Added for better connection monitoring
                    retryWrites=True,  # Enable retryable writes
                    retryReads=True,   # Enable retryable reads
                    w='majority'       # Write concern for data safety
                )
                
                # Test connection with timeout
                await asyncio.wait_for(
                    self.client.admin.command('ping'), 
                    timeout=10.0
                )
                
                self.database = self.client[self.settings.database_name]
                
                # Create indexes for optimization
                await self._create_indexes()
                
                logger.info("✅ Successfully connected to MongoDB Atlas")
                return
                
            except (ServerSelectionTimeoutError, NetworkTimeout, AutoReconnect) as e:
                logger.warning(f"⚠️ MongoDB connection attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("❌ Failed to connect to MongoDB Atlas after all retries")
                    raise ConnectionError("Unable to connect to database. Please check your internet connection.")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                logger.error(f"❌ Unexpected error connecting to MongoDB Atlas: {str(e)}")
                raise
    
    async def disconnect(self):
        """Close database connection"""
        if self.client:
            try:
                self.client.close()
                logger.info("✅ Disconnected from MongoDB Atlas")
            except Exception as e:
                logger.warning(f"⚠️ Error during disconnect: {str(e)}")
    
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
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to create some indexes: {str(e)}")
    
    def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance with connection validation"""
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database
    
    async def health_check(self) -> bool:
        """Check database health with timeout"""
        try:
            if self.client is None:
                return False
            await asyncio.wait_for(
                self.client.admin.command('ping'), 
                timeout=5.0
            )
            return True
        except Exception as e:
            logger.warning(f"⚠️ Database health check failed: {str(e)}")
            return False
    
    async def ensure_connection(self):
        """Ensure database connection is active, reconnect if needed"""
        try:
            if not await self.health_check():
                logger.info("🔄 Database connection lost, attempting to reconnect...")
                await self.connect()
        except Exception as e:
            logger.error(f"❌ Failed to ensure database connection: {str(e)}")
            raise


# Global database manager instance
db_manager = DatabaseManager()


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database instance with connection validation"""
    # Ensure connection is active
    await db_manager.ensure_connection()
    return db_manager.get_database()


async def init_database():
    """Initialize database connection"""
    await db_manager.connect()


async def close_database():
    """Close database connection"""
    await db_manager.disconnect() 