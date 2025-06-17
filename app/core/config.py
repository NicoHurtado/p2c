import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "Prompt2Course API"
    app_version: str = "1.0.0"
    app_env: str = Field(default="development", env="APP_ENV")
    secret_key: str = Field(..., env="SECRET_KEY")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"], 
        env="CORS_ORIGINS"
    )
    
    # MongoDB Atlas
    mongodb_atlas_uri: str = Field(..., env="MONGODB_ATLAS_URI")
    database_name: str = "prompt2course"
    
    # AI Services
    claude_api_key: str = Field(..., env="CLAUDE_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    
    # TTS Service (Amazon Polly)
    aws_polly_region: str = Field(default="us-east-1", env="AWS_POLLY_REGION")
    
    # YouTube API
    youtube_data_api_key: str = Field(..., env="YOUTUBE_DATA_API_KEY")
    
    # AWS Services (Required for Polly and S3)
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_s3_bucket: str = Field(default="prompt2course-audio-files", env="AWS_S3_BUCKET")
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Redis
    redis_url: str = Field(default="redis://invalid:6379", env="REDIS_URL")
    
    # Course Generation Settings
    max_chunk_size: int = 5000
    max_modules_per_course: int = 15
    min_modules_per_course: int = 5
    max_concepts_per_module: int = 8
    min_concepts_per_module: int = 3
    
    # Generation Timeouts (seconds)
    metadata_generation_timeout: int = 3
    module_generation_timeout: int = 30
    total_generation_timeout: int = 300
    
    # Cache TTL (seconds)
    course_cache_ttl: int = 3600  # 1 hour
    ai_response_cache_ttl: int = 86400  # 24 hours
    video_search_cache_ttl: int = 604800  # 1 week
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def get_mongodb_url(self) -> str:
        return self.mongodb_atlas_uri
    
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"
    
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    return Settings() 