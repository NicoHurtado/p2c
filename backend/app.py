from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db import init_db
from routes import auth, courses, subscription

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])

# Startup event to initialize database
@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup."""
    try:
        await init_db()
        print("Database connection established")
    except Exception as e:
        print(f"Failed to connect to database: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.VERSION,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "app": settings.APP_NAME
    }

# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    ) 