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
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
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
    
    # Payment settings (Wompi)
    WOMPI_PUBLIC_KEY: Optional[str] = os.getenv("WOMPI_PUBLIC_KEY")
    WOMPI_PRIVATE_KEY: Optional[str] = os.getenv("WOMPI_PRIVATE_KEY")
    WOMPI_EVENTS_KEY: Optional[str] = os.getenv("WOMPI_EVENTS_KEY")
    WOMPI_API_URL: str = os.getenv("WOMPI_API_URL", "https://sandbox.wompi.co/v1")
    
    # Feature flags
    PAYMENT_ENABLED: bool = os.getenv("PAYMENT_ENABLED", "True").lower() in ("true", "1", "t")
    SIMULATION_MODE: bool = os.getenv("SIMULATION_MODE", "True").lower() in ("true", "1", "t")
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.SECRET_KEY or self.SECRET_KEY == "your-secret-key-change-in-production":
            raise ValueError("SECRET_KEY must be set and not be the default value")
        
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set")
        
        if not self.MONGO_URI:
            raise ValueError("MONGO_URI must be set")

# Global settings instance
settings = Settings() 