from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import database connection
from db import init_db

# Import route modules
from routes import auth, courses, subscription

# Import document models
from models.user import User
from models.course import Course

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(title="Course Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000"), "*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from modules with explicit prefixes
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(courses.router, prefix="/api", tags=["Courses"])
app.include_router(subscription.router, prefix="/api", tags=["Subscription"])

# Startup event to initialize database
@app.on_event("startup")
async def startup_db_client():
    try:
        await init_db()
        print("Database connection established")
    except Exception as e:
        print(f"Failed to connect to database: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    return {"message": "Course Generator API is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "1.0.0"}

# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app", 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("DEBUG", "True").lower() in ("true", "1", "t"))
    ) 