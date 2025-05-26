from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import uuid
import logging
from datetime import datetime

from models.user import User
from utils.auth import get_current_user
from services.course import request_course_generation
from models.course import Course

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/generate-course")
async def generate_course(payload: Dict[str, Any], current_user: User = Depends(get_current_user)):
    """Generate a course using external API"""
    try:
        logger.info(f"Generating course for user {current_user.id} with payload: {payload}")
        
        # Validate required fields
        required_fields = ["prompt", "experience_level", "personality", "learning_style"]
        for field in required_fields:
            if field not in payload:
                logger.error(f"Missing required field: {field}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Add default intensity if not provided
        if "intensity" not in payload:
            payload["intensity"] = "medium"
            logger.info("Added default intensity: medium")
        
        # Validate field values
        valid_experience_levels = ["beginner", "intermediate", "advanced"]
        valid_personalities = ["analytical", "creative", "practical", "social"]
        valid_learning_styles = ["visual", "auditory", "kinesthetic", "interactive"]
        valid_intensities = ["short", "medium", "long"]
        
        if payload["experience_level"] not in valid_experience_levels:
            logger.error(f"Invalid experience_level: {payload['experience_level']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid experience_level. Must be one of: {', '.join(valid_experience_levels)}"
            )
        
        if payload["personality"] not in valid_personalities:
            logger.error(f"Invalid personality: {payload['personality']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid personality. Must be one of: {', '.join(valid_personalities)}"
            )
        
        if payload["learning_style"] not in valid_learning_styles:
            logger.error(f"Invalid learning_style: {payload['learning_style']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid learning_style. Must be one of: {', '.join(valid_learning_styles)}"
            )
        
        if payload["intensity"] not in valid_intensities:
            logger.error(f"Invalid intensity: {payload['intensity']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid intensity. Must be one of: {', '.join(valid_intensities)}"
            )
        
        logger.info("All validations passed, calling external API...")
        
        # Request course generation from external API
        course_data = await request_course_generation(payload)
        
        logger.info(f"Course generated successfully: {course_data.get('titulo', 'Unknown title')}")
        
        return course_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating course: {str(e)}"
        )

@router.post("/save")
async def save_course(course_data: Dict[str, Any], current_user: User = Depends(get_current_user)):
    """Save a generated course"""
    try:
        logger.info(f"Saving course for user {current_user.id}")
        
        # Create and save new course
        new_course = Course(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            title=course_data.get("titulo", course_data.get("title", "Untitled Course")),
            prompt=course_data.get("prompt", ""),
            content=course_data.get("content", course_data),
            experience_level=course_data.get("experience_level", "beginner"),
            available_time=course_data.get("available_time", course_data.get("duracion", "N/A"))
        )
        
        await new_course.insert()
        
        logger.info(f"Course saved successfully with ID: {new_course.id}")
        
        return {"id": new_course.id, "message": "Course saved successfully"}
        
    except Exception as e:
        logger.error(f"Error saving course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving course: {str(e)}"
        )

@router.get("/")
async def get_courses(current_user: User = Depends(get_current_user)):
    """Get all courses for current user"""
    try:
        courses = await Course.find(Course.user_id == current_user.id).to_list()
        
        course_list = [
            {
                "id": course.id,
                "title": course.title,
                "experience_level": course.experience_level,
                "available_time": course.available_time,
                "created_at": course.created_at.isoformat()
            }
            for course in courses
        ]
        
        return course_list
        
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching courses: {str(e)}"
        )

@router.get("/{course_id}")
async def get_course(course_id: str, current_user: User = Depends(get_current_user)):
    """Get a specific course by ID"""
    try:
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        return {
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "experience_level": course.experience_level,
            "available_time": course.available_time,
            "created_at": course.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching course: {str(e)}"
        )

@router.delete("/{course_id}")
async def delete_course(course_id: str, current_user: User = Depends(get_current_user)):
    """Delete a course"""
    try:
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        await course.delete()
        
        return {"success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course: {str(e)}"
        ) 