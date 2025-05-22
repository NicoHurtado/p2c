from typing import List, Dict, Any
import uuid
from fastapi import HTTPException, status, Depends

from models.user import User
from models.course import Course
from services.openai_service import generate_course_with_ai
from services.subscription_service import get_remaining_courses

class CourseController:
    """
    Controller for managing course-related operations
    """
    
    @staticmethod
    async def generate_course(topic: str, experience_level: str, available_time: str, current_user: User = None, is_demo: bool = False):
        """Generate a course with AI"""
        # Si es demo, no verificamos límites de suscripción
        if not is_demo and current_user:
            # Check remaining courses based on plan
            remaining_courses = await get_remaining_courses(current_user)
            
            if remaining_courses == 0:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You have reached your course limit for your plan"
                )
        
        # Build user profile for context if available
        user_profile = None
        if current_user and current_user.completed_setup:
            user_profile = {
                "preferences": current_user.preferences,
                "learning_style": current_user.learning_style,
                "personality": current_user.personality,
                "profile_type": current_user.profile_type
            }
        
        # Generate the course with AI
        course_content = await generate_course_with_ai(
            topic=topic,
            experience_level=experience_level,
            available_time=available_time,
            user_profile=user_profile
        )
        
        # Para versiones demo, limitamos a solo 2 módulos
        if is_demo and "modules" in course_content and len(course_content["modules"]) > 2:
            course_content["modules"] = course_content["modules"][:2]
            course_content["is_demo"] = True
            course_content["demo_message"] = "Esta es una versión demo. Regístrate para acceder a todos los módulos y características."
        
        return course_content

    @staticmethod
    async def save_course(
        title: str, 
        prompt: str, 
        content: Dict[str, Any], 
        experience_level: str, 
        available_time: str, 
        current_user: User
    ):
        """Save a generated course"""
        # Check remaining courses based on plan
        remaining_courses = await get_remaining_courses(current_user)
        
        if remaining_courses == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have reached your course limit for your plan"
            )
        
        # Create and save new course
        new_course = Course(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            title=title,
            prompt=prompt,
            content=content,
            experience_level=experience_level,
            available_time=available_time
        )
        
        await new_course.insert()
        
        return {"id": new_course.id, "message": "Course saved successfully"}
    
    @staticmethod
    async def get_user_courses(current_user: User):
        """Get all courses for the current user"""
        # Find all courses for the user
        courses = await Course.find(Course.user_id == current_user.id).to_list()
        
        # Format the response
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
    
    @staticmethod
    async def get_course_by_id(course_id: str, current_user: User):
        """Get a specific course by ID"""
        # Find the course
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        # Format the response
        return {
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "experience_level": course.experience_level,
            "available_time": course.available_time,
            "created_at": course.created_at.isoformat()
        }
    
    @staticmethod
    async def delete_course(course_id: str, current_user: User):
        """Delete a course"""
        # Find the course
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        # Delete the course
        await course.delete()
        
        return {"success": True}
    
    @staticmethod
    async def replace_topic(course_id: str, section: str, current_topic: str, experience_level: str, current_user: User):
        """Replace a specific topic in a course with AI-generated content"""
        # Find the course
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        # Generate a new section with AI
        prompt = f"Rewrite the following section in a {experience_level} level for {course.title}: {current_topic}"
        
        # Build user profile for context if available
        user_profile = None
        if current_user.completed_setup:
            user_profile = {
                "preferences": current_user.preferences,
                "learning_style": current_user.learning_style,
                "personality": current_user.personality,
                "profile_type": current_user.profile_type
            }
        
        # Basic generation for this example
        response = await generate_course_with_ai(
            topic=f"Rewrite section: {current_topic}",
            experience_level=experience_level,
            available_time="N/A",
            user_profile=user_profile
        )
        
        # Return the generated content
        return {
            "original": current_topic,
            "replacement": response.get("summary", "Failed to generate replacement"),
            "success": True
        }
    
    @staticmethod
    async def replace_module(course_id: str, module_index: int, current_module_title: str, experience_level: str, current_user: User):
        """Replace a specific module in a course with AI-generated content"""
        # Find the course
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        # Generate a new module with AI
        prompt = f"Rewrite the following module in a {experience_level} level for {course.title}: {current_module_title}"
        
        # Build user profile for context if available
        user_profile = None
        if current_user.completed_setup:
            user_profile = {
                "preferences": current_user.preferences,
                "learning_style": current_user.learning_style,
                "personality": current_user.personality,
                "profile_type": current_user.profile_type
            }
        
        # Basic generation for this example
        response = await generate_course_with_ai(
            topic=f"Rewrite module: {current_module_title}",
            experience_level=experience_level,
            available_time="N/A",
            user_profile=user_profile
        )
        
        # Extract just the first module from the response
        if response and "modules" in response and len(response["modules"]) > 0:
            new_module = response["modules"][0]
        else:
            new_module = {
                "title": f"Revised: {current_module_title}",
                "steps": ["Failed to generate new module content"],
                "example": ""
            }
        
        # Return the generated content
        return {
            "original_title": current_module_title,
            "new_module": new_module,
            "success": True
        }
        
    @staticmethod
    async def complete_module(course_id: str, module_id: str, current_user: User):
        """Mark a module as completed"""
        # Find the course
        course = await Course.find_one(Course.id == course_id, Course.user_id == current_user.id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found or access denied"
            )
        
        # Update course progress
        if not hasattr(course, 'progress'):
            course.progress = {'completed_modules': []}
            
        # Check if we already have a progress field, if not, create it
        if not hasattr(course, 'progress') or not course.progress:
            course.progress = {'completed_modules': []}
        
        # Add module to completed list if not already there
        if module_id not in course.progress['completed_modules']:
            course.progress['completed_modules'].append(module_id)
            await course.save()
            
        return {
            "success": True,
            "completed_modules": course.progress['completed_modules']
        } 