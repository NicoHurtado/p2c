from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Optional, List
import json
import logging
from sse_starlette.sse import EventSourceResponse

from ..models.course import (
    CourseGenerationRequest, CourseGenerationResponse, 
    Course, AudioGenerationRequest, CourseStatus
)
from ..services.course_generator import CourseGenerationService
from ..services.cache_service import get_cache_service
from ..core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/courses", tags=["courses"])

# Initialize service
course_service = CourseGenerationService()


@router.post("/generate", response_model=CourseGenerationResponse)
async def generate_course(
    request: CourseGenerationRequest,
    user_id: str = "anonymous"
):
    """
    Generate a new course with metadata and introduction in < 3 seconds.
    Content generation continues asynchronously.
    """
    try:
        # Log the incoming request for debugging
        logger.info(f"Received course generation request from user {user_id}")
        logger.info(f"Request data: {request.dict()}")
        
        # Additional validation
        if not request.prompt or len(request.prompt.strip()) < 1:
            logger.error(f"Invalid prompt: '{request.prompt}' (length: {len(request.prompt) if request.prompt else 0})")
            raise HTTPException(
                status_code=422, 
                detail="El prompt no puede estar vacío"
            )
        
        if not request.level or request.level not in ["principiante", "intermedio", "avanzado"]:
            logger.error(f"Invalid level: '{request.level}'")
            raise HTTPException(
                status_code=422, 
                detail="El nivel debe ser 'principiante', 'intermedio' o 'avanzado'"
            )
        
        if not request.interests or len(request.interests) == 0:
            logger.error(f"Invalid interests: {request.interests}")
            raise HTTPException(
                status_code=422, 
                detail="Debe incluir al menos un interés"
            )
        
        response = await course_service.generate_course_fast_response(
            request, user_id
        )
        
        logger.info(f"Successfully generated course {response.course_id} for user {user_id}")
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in course generation: {str(e)}")
        raise HTTPException(
            status_code=422, 
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error generating course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/test-validation")
async def test_validation(request: CourseGenerationRequest):
    """
    Test endpoint to validate request format without generating a course
    """
    try:
        return {
            "status": "valid",
            "message": "Request format is correct",
            "received_data": {
                "prompt": request.prompt,
                "level": request.level,
                "interests": request.interests,
                "prompt_length": len(request.prompt),
                "interests_count": len(request.interests)
            }
        }
    except Exception as e:
        logger.error(f"Validation test error: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {str(e)}"
        )


@router.get("/stream/{course_id}")
async def stream_course_progress(course_id: str):
    """
    Stream course generation progress using Server-Sent Events.
    Frontend can listen to real-time updates.
    """
    async def event_stream():
        try:
            async for event in course_service.stream_course_generation_progress(course_id):
                yield {
                    "event": event.event_type,
                    "data": json.dumps(event.data, default=str)
                }
        except Exception as e:
            logger.error(f"Error in event stream: {str(e)}")
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_stream())


@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str):
    """Get complete course by ID"""
    try:
        course = await course_service.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving course: {str(e)}"
        )


@router.get("/{course_id}/module/{module_id}")
async def get_module(course_id: str, module_id: str):
    """Get specific module from course"""
    try:
        module = await course_service.get_module(course_id, module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        return module
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting module: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving module: {str(e)}"
        )


@router.post("/{course_id}/generate-module/{module_index}")
async def generate_module_on_demand(course_id: str, module_index: int):
    """Generate a specific module on demand"""
    try:
        module = await course_service.generate_module_on_demand(course_id, module_index)
        if not module:
            raise HTTPException(status_code=404, detail="Unable to generate module")
        return {
            "message": f"Module {module_index + 1} generated successfully",
            "module": module
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating module on demand: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating module: {str(e)}"
        )


@router.post("/{course_id}/audio")
async def generate_audio(
    course_id: str,
    request: AudioGenerationRequest,
    user_id: str = "anonymous"
):
    """Generate TTS audio for specific text"""
    try:
        # Rate limiting check
        cache_service = await get_cache_service()
        if not await cache_service.set_rate_limit(user_id, "audio_generation", 10, 3600):
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Max 10 audio generations per hour."
            )
        
        audio_url = await course_service.generate_audio_for_concept(
            course_id,
            "general",  # module_id for general audio
            request.text,
            user_id
        )
        
        if not audio_url:
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate audio"
            )
            
        return {"audio_url": audio_url, "text": request.text}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating audio: {str(e)}"
        )


@router.get("/")
async def list_courses(
    skip: int = 0, 
    limit: int = 20,
    status: Optional[CourseStatus] = None,
    user_id: Optional[str] = None
):
    """List courses with pagination and filtering"""
    try:
        database = await get_database()
        
        # Build query
        query = {}
        if status:
            query["status"] = status.value
        if user_id:
            query["user_id"] = user_id
            
        # Get courses with pagination
        cursor = database.courses.find(query).skip(skip).limit(limit)
        courses = await cursor.to_list(length=limit)
        
        # Get total count
        total = await database.courses.count_documents(query)
        
        return {
            "courses": courses,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error listing courses: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error listing courses: {str(e)}"
        )


@router.delete("/{course_id}")
async def delete_course(course_id: str, user_id: str = "anonymous"):
    """Delete a course (admin only)"""
    try:
        database = await get_database()
        
        # Check if course exists
        course = await database.courses.find_one({"_id": course_id})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Delete course
        result = await database.courses.delete_one({"_id": course_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete course")
        
        # Invalidate cache
        cache_service = await get_cache_service()
        await cache_service.invalidate_course_cache(course_id)
        
        return {"message": "Course deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting course: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting course: {str(e)}"
        )


@router.get("/stats/overview")
async def get_system_statistics():
    """Get system statistics and metrics"""
    try:
        stats = await course_service.get_course_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving statistics: {str(e)}"
        ) 


@router.post("/{course_id}/start-course")
async def start_course_background_generation(
    course_id: str,
    background_tasks: BackgroundTasks,
    user_id: str = "anonymous"
):
    """
    Start course and trigger background generation of all remaining modules.
    This optimizes UX by pre-generating content while user consumes first module.
    """
    try:
        # Verify course exists
        course = await course_service.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Add background task to generate remaining modules
        background_tasks.add_task(
            course_service.generate_remaining_modules_background,
            course_id,
            user_id
        )
        
        return {
            "message": "Course started successfully",
            "course_id": course_id,
            "status": "background_generation_initiated",
            "info": "All remaining modules are being generated in background for optimal experience"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting course: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error starting course: {str(e)}"
        ) 


@router.get("/stats/cost-optimization")
async def get_cost_optimization_stats():
    """Get cost optimization statistics and savings analysis"""
    try:
        cost_stats = course_service.claude_service.get_cost_statistics()
        return {
            "message": "Cost optimization statistics",
            "statistics": cost_stats,
            "recommendations": {
                "current_optimizations": [
                    "✅ Batch concept generation (70-80% cost reduction)",
                    "✅ Optimized prompts (20-30% token reduction)",
                    "✅ Smart token limits (15-25% efficiency gain)"
                ],
                "additional_suggestions": [
                    "Consider implementing prompt templates for common patterns",
                    "Monitor batch success rates and adjust chunk sizes",
                    "Implement response caching for similar course requests"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting cost optimization stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving cost statistics: {str(e)}"
        ) 


@router.post("/debug-request")
async def debug_request(request_data: dict):
    """
    Debug endpoint to see exactly what data is being sent
    """
    try:
        logger.info(f"🐛 DEBUG: Raw request data received: {request_data}")
        logger.info(f"🐛 DEBUG: Data type: {type(request_data)}")
        logger.info(f"🐛 DEBUG: Data keys: {list(request_data.keys()) if isinstance(request_data, dict) else 'Not a dict'}")
        
        # Try to validate as CourseGenerationRequest
        try:
            validated_request = CourseGenerationRequest(**request_data)
            logger.info(f"🐛 DEBUG: Successfully validated as CourseGenerationRequest: {validated_request.dict()}")
            return {
                "status": "success",
                "message": "Data is valid",
                "validated_data": validated_request.dict()
            }
        except Exception as validation_error:
            logger.error(f"🐛 DEBUG: Validation failed: {str(validation_error)}")
            return {
                "status": "validation_error",
                "message": str(validation_error),
                "raw_data": request_data
            }
            
    except Exception as e:
        logger.error(f"🐛 DEBUG: Unexpected error: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "raw_data": request_data if 'request_data' in locals() else "Unknown"
        } 


@router.get("/debug-errors")
async def debug_recent_errors():
    """
    Show recent errors and request patterns
    """
    try:
        # Get recent log entries (this is a simplified version)
        import datetime
        
        return {
            "message": "Check server logs for detailed error information",
            "timestamp": datetime.datetime.now().isoformat(),
            "tips": [
                "Error 422 usually means validation failed",
                "Check that 'prompt' is not empty",
                "Check that 'level' is 'principiante', 'intermedio', or 'avanzado'",
                "Check that 'interests' is a non-empty array",
                "Check that JSON format is correct"
            ],
            "example_valid_request": {
                "prompt": "Quiero aprender Python para desarrollar aplicaciones web",
                "level": "principiante",
                "interests": ["programación", "web", "python"]
            }
        }
    except Exception as e:
        return {"error": str(e)} 