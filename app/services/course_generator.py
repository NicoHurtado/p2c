import asyncio
import logging
import uuid
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json

from ..models.course import (
    Course, CourseMetadata, Module, ModuleChunk, 
    CourseLevel, CourseStatus, CourseGenerationRequest,
    CourseGenerationResponse, StreamEvent, FinalProject
)
from ..core.database import get_database
from .claude_service import ClaudeService
from .youtube_service import YouTubeService
from .elevenlabs_service import ElevenLabsService
from .cache_service import CacheService

logger = logging.getLogger(__name__)


class CourseGenerationService:
    """Main service for intelligent course generation with optimization"""
    
    def __init__(self):
        self.claude_service = ClaudeService()
        self.youtube_service = YouTubeService()
        self.tts_service = ElevenLabsService()
        self.cache_service = CacheService()
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    async def generate_course_fast_response(
        self, 
        request: CourseGenerationRequest,
        user_id: str = "anonymous"
    ) -> CourseGenerationResponse:
        """Generate course metadata and introduction in < 3 seconds"""
        
        try:
            logger.info(f"Starting fast course generation for user {user_id}")
            start_time = datetime.utcnow()
            
            # Check cache first
            cached_response = await self.cache_service.get_cached_ai_response(
                request.prompt,
                "claude",
                request.level.value,
                request.interests
            )
            
            if cached_response and "metadata" in cached_response.get("response", {}):
                logger.info("Using cached course metadata")
                metadata = CourseMetadata(**cached_response["response"]["metadata"])
                course_id = str(uuid.uuid4())
            else:
                # Generate fresh metadata
                metadata = await self.claude_service.generate_course_metadata(
                    request.prompt,
                    request.level,
                    request.interests
                )
                
                # Cache the response
                await self.cache_service.cache_ai_response(
                    request.prompt,
                    {"metadata": metadata.dict()},
                    "claude",
                    request.level.value,
                    request.interests
                )
            
            # Create course with initial data
            course_id = str(uuid.uuid4())
            course = Course(
                id=course_id,
                metadata=metadata,
                user_prompt=request.prompt,
                user_level=request.level,
                user_interests=request.interests,
                status=CourseStatus.GENERATING
            )
            
            # Save initial course to database
            database = await get_database()
            course_dict = course.dict(by_alias=True)
            course_dict["_id"] = course_id
            await database.courses.insert_one(course_dict)
            
            # Start async content generation (don't wait)
            asyncio.create_task(
                self._generate_course_content_async(course_id, course, user_id)
            )
            
            # Log timing
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Fast response generated in {elapsed:.2f} seconds")
            
            return CourseGenerationResponse(
                course_id=course_id,
                metadata=metadata,
                status=CourseStatus.GENERATING,
                introduction_ready=True
            )
            
        except Exception as e:
            logger.error(f"Error in fast course generation: {str(e)}")
            raise
    
    async def _generate_course_content_async(
        self, 
        course_id: str, 
        course: Course, 
        user_id: str
    ):
        """Generate course introduction and first module only"""
        
        try:
            logger.info(f"Starting async content generation for course {course_id}")
            
            # Generate introduction
            introduction = await self.claude_service.generate_course_introduction(
                course.metadata,
                course.user_prompt,
                course.user_interests
            )
            
            # Update course with introduction
            await self._update_course_introduction(course_id, introduction)
            
            # Generate ONLY the first module
            if course.metadata.module_list:
                try:
                    first_module_title = course.metadata.module_list[0]
                    logger.info(f"Generating first module: {first_module_title}")
                    
                    # Generate module structure first
                    module_structure = await self.claude_service.generate_module_structure(
                        first_module_title,
                        course.user_prompt,
                        course.user_level,
                        course.user_interests,
                        0
                    )
                    
                    # Generate module content in chunks
                    chunks = await self.claude_service.generate_module_content_chunked(
                        module_structure,
                        course.user_prompt,
                        course.user_level,
                        course.user_interests
                    )
                    
                    # Search for relevant videos
                    videos = await self.youtube_service.search_videos_for_module(
                        first_module_title,
                        module_structure["concepts"],
                        course.user_prompt
                    )
                    
                    # Create module
                    module = Module(
                        module_id=module_structure["module_id"],
                        title=module_structure["title"],
                        description=module_structure["description"],
                        objective=module_structure["objective"],
                        concepts=module_structure["concepts"],
                        chunks=chunks,
                        quiz=module_structure["quiz"],
                        summary=module_structure["summary"],
                        practical_exercise=module_structure["practical_exercise"]
                    )
                    
                    # Add videos to module resources
                    for video in videos:
                        module.resources.videos.append(video)
                    
                    # Save first module to database
                    await self._save_module_to_course(course_id, module)
                    
                    logger.info(f"First module completed: {first_module_title}")
                    
                except Exception as e:
                    logger.error(f"Error generating first module: {str(e)}")
            
            # Mark course as ready with first module
            await self._mark_course_ready(course_id)
            
            # Cache completed course
            await self.cache_service.cache_course(course_id, {"status": "ready"})
            
            logger.info(f"Course {course_id} initial generation completed (intro + first module)")
            
        except Exception as e:
            logger.error(f"Error in async course generation: {str(e)}")
            await self._mark_course_error(course_id, str(e))
    
    async def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID with caching"""
        
        try:
            # Check cache first
            cached_course = await self.cache_service.get_cached_course(course_id)
            if cached_course:
                course_data = cached_course["course"]
                return Course(**course_data)
            
            # Get from database
            database = await get_database()
            course_doc = await database.courses.find_one({"_id": course_id})
            
            if course_doc:
                course = Course(**course_doc)
                
                # Cache for future requests
                await self.cache_service.cache_course(course_id, course.dict())
                
                return course
                
        except Exception as e:
            logger.error(f"Error getting course {course_id}: {str(e)}")
            
        return None
    
    async def get_module(self, course_id: str, module_id: str) -> Optional[Module]:
        """Get specific module from course"""
        
        try:
            course = await self.get_course(course_id)
            if course:
                for module in course.modules:
                    if module.module_id == module_id:
                        return module
                        
        except Exception as e:
            logger.error(f"Error getting module {module_id}: {str(e)}")
            
        return None
    
    async def generate_module_on_demand(
        self, 
        course_id: str, 
        module_index: int
    ) -> Optional[Module]:
        """Generate a specific module on demand"""
        
        try:
            # Get course to check if module already exists
            course = await self.get_course(course_id)
            if not course:
                logger.error(f"Course {course_id} not found")
                return None
            
            # Check if module already exists
            if len(course.modules) > module_index:
                logger.info(f"Module {module_index} already exists for course {course_id}")
                return course.modules[module_index]
            
            # Check if module_index is valid
            if module_index >= len(course.metadata.module_list):
                logger.error(f"Module index {module_index} out of range for course {course_id}")
                return None
                
            module_title = course.metadata.module_list[module_index]
            logger.info(f"Generating module {module_index + 1}: {module_title} for course {course_id}")
            
            # Generate module structure
            module_structure = await self.claude_service.generate_module_structure(
                module_title,
                course.user_prompt,
                course.user_level,
                course.user_interests,
                module_index
            )
            
            # Generate module content in chunks
            chunks = await self.claude_service.generate_module_content_chunked(
                module_structure,
                course.user_prompt,
                course.user_level,
                course.user_interests
            )
            
            # Search for relevant videos
            videos = await self.youtube_service.search_videos_for_module(
                module_title,
                module_structure["concepts"],
                course.user_prompt
            )
            
            # Create module
            module = Module(
                module_id=module_structure["module_id"],
                title=module_structure["title"],
                description=module_structure["description"],
                objective=module_structure["objective"],
                concepts=module_structure["concepts"],
                chunks=chunks,
                quiz=module_structure["quiz"],
                summary=module_structure["summary"],
                practical_exercise=module_structure["practical_exercise"]
            )
            
            # Add videos to module resources
            for video in videos:
                module.resources.videos.append(video)
            
            # Save module to database
            await self._save_module_to_course(course_id, module)
            
            # Invalidate cache to ensure fresh data
            await self.cache_service.invalidate_course_cache(course_id)
            
            logger.info(f"Module {module_index + 1} generated successfully for course {course_id}")
            return module
            
        except Exception as e:
            logger.error(f"Error generating module {module_index} for course {course_id}: {str(e)}")
            return None
    
    async def generate_audio_for_concept(
        self, 
        course_id: str, 
        module_id: str, 
        concept_text: str,
        user_id: str
    ) -> Optional[str]:
        """Generate TTS audio for a specific concept"""
        
        try:
            audio_resource = await self.tts_service.generate_audio_for_concept(
                concept_text,
                user_id,
                f"{course_id}_{module_id}"
            )
            
            if audio_resource:
                # Save audio resource to course
                await self._add_audio_to_module(course_id, module_id, audio_resource)
                return audio_resource.s3_url
                
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            
        return None
    
    async def stream_course_generation_progress(
        self, 
        course_id: str
    ) -> AsyncGenerator[StreamEvent, None]:
        """Stream course generation progress using Server-Sent Events"""
        
        try:
            # Initial status
            course = await self.get_course(course_id)
            if not course:
                yield StreamEvent(
                    event_type="error",
                    data={"message": "Course not found"}
                )
                return
            
            yield StreamEvent(
                event_type="course_started",
                data={
                    "course_id": course_id,
                    "total_modules": course.metadata.total_modules,
                    "status": course.status.value
                }
            )
            
            # Monitor progress
            completed_modules = set()
            
            while course.status == CourseStatus.GENERATING:
                await asyncio.sleep(2)  # Check every 2 seconds
                
                # Check module progress
                for i, module_title in enumerate(course.metadata.module_list):
                    module_id = f"modulo_{i + 1}"
                    
                    if module_id not in completed_modules:
                        progress = await self.cache_service.get_module_generation_progress(
                            course_id, module_id
                        )
                        
                        if progress and progress.get("status") == "completed":
                            completed_modules.add(module_id)
                            
                            yield StreamEvent(
                                event_type="module_ready",
                                data={
                                    "module_id": module_id,
                                    "module_title": module_title,
                                    "progress": progress.get("progress", 0),
                                    "completed_modules": len(completed_modules),
                                    "total_modules": course.metadata.total_modules
                                }
                            )
                
                # Check if course is complete
                course = await self.get_course(course_id)
                if course.status == CourseStatus.READY:
                    yield StreamEvent(
                        event_type="course_complete",
                        data={
                            "course_id": course_id,
                            "status": "ready",
                            "completed_modules": len(completed_modules),
                            "total_modules": course.metadata.total_modules
                        }
                    )
                    break
                elif course.status == CourseStatus.ERROR:
                    yield StreamEvent(
                        event_type="error",
                        data={
                            "course_id": course_id,
                            "message": "Course generation failed"
                        }
                    )
                    break
                    
        except Exception as e:
            logger.error(f"Error streaming progress: {str(e)}")
            yield StreamEvent(
                event_type="error",
                data={"message": str(e)}
            )
    
    async def _update_course_introduction(self, course_id: str, introduction: str):
        """Update course with introduction"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {"$set": {"introduction": introduction}}
        )
        
        # Invalidate cache
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _save_module_to_course(self, course_id: str, module: Module):
        """Save module to course in database"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {"$push": {"modules": module.dict()}}
        )
        
        # Invalidate cache
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _update_course_final_project(self, course_id: str, final_project: FinalProject):
        """Update course with final project"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {"$set": {"final_project": final_project.dict()}}
        )
        
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _update_course_summary(self, course_id: str, summary: str):
        """Update course with summary"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {"$set": {"summary": summary}}
        )
        
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _mark_course_ready(self, course_id: str):
        """Mark course as ready"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {"$set": {"status": CourseStatus.READY.value}}
        )
        
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _mark_course_error(self, course_id: str, error_message: str):
        """Mark course as error"""
        database = await get_database()
        await database.courses.update_one(
            {"_id": course_id},
            {
                "$set": {
                    "status": CourseStatus.ERROR.value,
                    "error_message": error_message
                }
            }
        )
        
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def _add_audio_to_module(
        self, 
        course_id: str, 
        module_id: str, 
        audio_resource
    ):
        """Add audio resource to module"""
        database = await get_database()
        await database.courses.update_one(
            {
                "_id": course_id,
                "modules.module_id": module_id
            },
            {
                "$push": {
                    "modules.$.resources.audios": audio_resource.dict()
                }
            }
        )
        
        await self.cache_service.invalidate_course_cache(course_id)
    
    async def get_course_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        
        try:
            database = await get_database()
            
            # Course statistics
            total_courses = await database.courses.count_documents({})
            ready_courses = await database.courses.count_documents(
                {"status": CourseStatus.READY.value}
            )
            generating_courses = await database.courses.count_documents(
                {"status": CourseStatus.GENERATING.value}
            )
            
            # Popular topics
            pipeline = [
                {"$unwind": "$user_interests"},
                {"$group": {"_id": "$user_interests", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            popular_interests = await database.courses.aggregate(pipeline).to_list(10)
            
            # Cache statistics
            cache_stats = await self.cache_service.get_cache_stats()
            
            return {
                "courses": {
                    "total": total_courses,
                    "ready": ready_courses,
                    "generating": generating_courses,
                    "error": total_courses - ready_courses - generating_courses
                },
                "popular_interests": popular_interests,
                "cache": cache_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {} 
    
    async def generate_remaining_modules_background(
        self, 
        course_id: str,
        user_id: str = "anonymous"
    ) -> bool:
        """
        Generate all remaining modules in background when user starts the course.
        This provides zero-latency experience for module navigation.
        """
        try:
            logger.info(f"Starting background generation of remaining modules for course {course_id}")
            
            # Get course to check current state
            course = await self.get_course(course_id)
            if not course:
                logger.error(f"Course {course_id} not found")
                return False
            
            # Determine which modules need to be generated
            current_modules = len(course.modules)
            total_modules = course.metadata.total_modules
            
            if current_modules >= total_modules:
                logger.info(f"All modules already generated for course {course_id}")
                return True
            
            logger.info(f"Generating {total_modules - current_modules} remaining modules in background")
            
            # Generate remaining modules concurrently (but limit concurrency to avoid overload)
            semaphore = asyncio.Semaphore(3)  # Max 3 concurrent module generations
            
            tasks = []
            for module_index in range(current_modules, total_modules):
                task = self._generate_single_module_with_semaphore(
                    semaphore, course_id, course, module_index
                )
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log results
            successful_modules = sum(1 for result in results if not isinstance(result, Exception))
            failed_modules = len(results) - successful_modules
            
            logger.info(f"Background generation completed: {successful_modules} successful, {failed_modules} failed")
            
            # Update course status if all modules are ready
            if successful_modules == len(tasks):
                database = await get_database()
                await database.courses.update_one(
                    {"_id": course_id},
                    {"$set": {"status": CourseStatus.READY.value, "all_modules_ready": True}}
                )
                
                # Invalidate cache
                await self.cache_service.invalidate_course_cache(course_id)
                
                logger.info(f"Course {course_id} marked as fully ready")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in background module generation: {str(e)}")
            return False
    
    async def _generate_single_module_with_semaphore(
        self,
        semaphore: asyncio.Semaphore,
        course_id: str,
        course: Course,
        module_index: int
    ) -> Optional[Module]:
        """Generate a single module with semaphore control"""
        
        async with semaphore:
            try:
                module_title = course.metadata.module_list[module_index]
                logger.info(f"Generating background module {module_index + 1}: {module_title}")
                
                # Update progress cache
                await self.cache_service.cache_module_generation_progress(
                    course_id, 
                    f"modulo_{module_index + 1}",
                    {"status": "generating", "progress": 0}
                )
                
                # Generate module structure
                module_structure = await self.claude_service.generate_module_structure(
                    module_title,
                    course.user_prompt,
                    course.user_level,
                    course.user_interests,
                    module_index
                )
                
                # Update progress
                await self.cache_service.cache_module_generation_progress(
                    course_id, 
                    f"modulo_{module_index + 1}",
                    {"status": "generating", "progress": 30}
                )
                
                # Generate module content in chunks
                chunks = await self.claude_service.generate_module_content_chunked(
                    module_structure,
                    course.user_prompt,
                    course.user_level,
                    course.user_interests
                )
                
                # Update progress
                await self.cache_service.cache_module_generation_progress(
                    course_id, 
                    f"modulo_{module_index + 1}",
                    {"status": "generating", "progress": 70}
                )
                
                # Search for relevant videos (async, don't block)
                videos = await self.youtube_service.search_videos_for_module(
                    module_title,
                    module_structure["concepts"],
                    course.user_prompt
                )
                
                # Create module
                module = Module(
                    module_id=module_structure["module_id"],
                    title=module_structure["title"],
                    description=module_structure["description"],
                    objective=module_structure["objective"],
                    concepts=module_structure["concepts"],
                    chunks=chunks,
                    quiz=module_structure["quiz"],
                    summary=module_structure["summary"],
                    practical_exercise=module_structure["practical_exercise"]
                )
                
                # Add videos to module resources
                for video in videos:
                    module.resources.videos.append(video)
                
                # Save module to database
                await self._save_module_to_course(course_id, module)
                
                # Mark as completed
                await self.cache_service.cache_module_generation_progress(
                    course_id, 
                    f"modulo_{module_index + 1}",
                    {"status": "completed", "progress": 100}
                )
                
                logger.info(f"Background module {module_index + 1} completed successfully")
                return module
                
            except Exception as e:
                logger.error(f"Error generating background module {module_index + 1}: {str(e)}")
                
                # Mark as failed
                await self.cache_service.cache_module_generation_progress(
                    course_id, 
                    f"modulo_{module_index + 1}",
                    {"status": "failed", "progress": 0, "error": str(e)}
                )
                return None 