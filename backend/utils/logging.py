"""
Logging configuration for the Course Generator API
"""

import logging
import sys
from typing import Optional
from config import settings


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration for the application
    """
    # Determine log level
    if level is None:
        level = "DEBUG" if settings.DEBUG else "INFO"
    
    # Create logger
    logger = logging.getLogger("course_generator")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    """
    return logging.getLogger(f"course_generator.{name}")


# Create default logger instance
logger = setup_logging() 