import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import json

from .core.config import get_settings
from .core.database import init_database, close_database
from .services.cache_service import init_cache, close_cache
from .api.courses import router as courses_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    
    # Startup
    logger.info("Starting Prompt2Course API...")
    
    try:
        # Initialize database connection
        await init_database()
        logger.info("Database connected successfully")
        
        # Initialize cache connection (optional for development)
        try:
            await init_cache()
            logger.info("Cache connected successfully")
        except Exception as e:
            logger.warning(f"Cache connection failed, continuing without cache: {str(e)}")
            logger.warning("Install Redis or use Docker for full functionality")
        
        logger.info("Prompt2Course API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Prompt2Course API...")
    
    try:
        # Close cache connection
        try:
            await close_cache()
            logger.info("Cache disconnected")
        except Exception as e:
            logger.warning(f"Cache disconnect failed: {str(e)}")
        
        # Close database connection
        await close_database()
        logger.info("Database disconnected")
        
        logger.info("Prompt2Course API shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="Prompt2Course API",
    description="""
    🚀 **Prompt2Course - Sistema Inteligente de Generación de Cursos**
    
    Una API avanzada que genera cursos educativos completos y personalizados usando IA.
    
    ## Características principales:
    
    * **⚡ Generación ultrarrápida**: Metadatos e introducción en < 3 segundos
    * **🧠 IA optimizada**: Integración con Claude para contenido inteligente
    * **📚 Chunking inteligente**: División optimizada del contenido para mejor rendimiento
    * **🎥 Videos automáticos**: Búsqueda e integración automática de videos de YouTube
    * **🔊 Audio TTS**: Generación de audio con ElevenLabs
    * **⚡ Streaming en tiempo real**: Server-Sent Events para progreso en vivo
    * **💾 Cache inteligente**: Redis para optimización de respuestas
    * **📊 Escalabilidad**: Diseñado para miles de usuarios simultáneos
    
    ## Flujo de uso:
    
    1. **POST /api/courses/generate** - Generar curso (respuesta inmediata)
    2. **GET /api/courses/stream/{course_id}** - Seguir progreso en tiempo real
    3. **GET /api/courses/{course_id}** - Obtener curso completo
    4. **POST /api/courses/{course_id}/audio** - Generar audio para conceptos
    
    ## Ejemplo de entrada:
    
    ```json
    {
      "prompt": "Quiero aprender inteligencia artificial para mis proyectos",
      "level": "principiante",
      "interests": ["deportes", "tenis", "videojuegos", "programación"]
    }
    ```
    
    El sistema conectará automáticamente los conceptos de IA con los intereses del usuario,
    creando ejemplos prácticos como análisis de partidos de tenis con IA o algoritmos
    para videojuegos.
    """,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add request logging middleware for debugging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request details
    logger.info(f"🔥 {request.method} {request.url}")
    logger.info(f"🔥 Headers: {dict(request.headers)}")
    
    # Process the request
    response = await call_next(request)
    
    # Log response details
    process_time = time.time() - start_time
    logger.info(f"🔥 Response status: {response.status_code} (took {process_time:.2f}s)")
    
    return response

# Include routers
app.include_router(courses_router)

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from .core.database import db_manager
        from .services.cache_service import cache_service
        
        # Check database health
        db_healthy = await db_manager.health_check()
        
        # Check cache health
        cache_healthy = cache_service.redis_client is not None
        if cache_healthy:
            try:
                await cache_service.redis_client.ping()
            except:
                cache_healthy = False
        
        return {
            "status": "healthy" if db_healthy and cache_healthy else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "cache": "connected" if cache_healthy else "disconnected",
            "version": settings.app_version,
            "environment": settings.app_env
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🚀 Prompt2Course API - Sistema Inteligente de Generación de Cursos",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "features": [
            "Generación ultrarrápida de cursos",
            "Personalización basada en intereses",
            "Integración con YouTube y TTS",
            "Streaming de progreso en tiempo real",
            "Cache inteligente para optimización"
        ]
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "request_id": str(id(request))
        }
    )

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler for HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development(),
        log_level=settings.log_level.lower()
    ) 