import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # Database settings
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "course_generator")
    
    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # App settings
    APP_NAME: str = "Course Generator API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS: list = [
        FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in environment variables")
        
        if len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        
        if not self.MONGO_URI:
            raise ValueError("MONGO_URI must be set")
    

# Global settings instance
settings = Settings() 