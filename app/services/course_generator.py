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
    CourseGenerationResponse, StreamEvent, FinalProject, PracticalExercise,
    ModuleMetadata
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
        """Generate course metadata and ALL modules metadata in < 3 seconds"""
        
        try:
            logger.info(f"🚀 Starting ENHANCED course generation for user {user_id}")
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
            else:
                # Generate fresh metadata (structure only, interests don't affect this)
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
            
            # 🎯 GENERATE COMPLETE METADATA FOR ALL MODULES (fast, no content yet)
            modules_metadata = []
            for i, module_title in enumerate(metadata.module_list):
                module_meta = ModuleMetadata(
                    module_id=f"modulo_{i + 1}",
                    title=module_title,
                    description=f"Módulo completo sobre {module_title} con teoría profunda y aplicaciones prácticas.",
                    objective=f"Al finalizar este módulo, dominarás {module_title} y podrás aplicarlo en proyectos reales.",
                    estimated_duration=2,
                    total_concepts=4
                )
                modules_metadata.append(module_meta)
            
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
            
            # Initialize modules array with empty slots for each module
            course_dict["modules"] = [None] * metadata.total_modules
            
            await database.courses.insert_one(course_dict)
            
            # 🔥 Start PARALLEL content generation for ALL modules (don't wait)
            asyncio.create_task(
                self._generate_course_content_async(course_id, course, user_id)
            )
            
            # Log timing
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"🎯 ENHANCED fast response generated in {elapsed:.2f} seconds")
            logger.info(f"📊 Returning metadata for {len(modules_metadata)} modules")
            
            return CourseGenerationResponse(
                course_id=course_id,
                metadata=metadata,
                modules_metadata=modules_metadata,  # Complete metadata for ALL modules
                status=CourseStatus.GENERATING,
                introduction_ready=True,
                generation_started=True,
                estimated_completion_time=len(modules_metadata) * 2  # 2 min per module
            )
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced course generation: {str(e)}")
            raise
    
    async def _generate_course_content_async(
        self, 
        course_id: str, 
        course: Course, 
        user_id: str
    ):
        """Generate ALL modules concurrently in parallel - TRUE async generation"""
        
        try:
            logger.info(f"🚀 Starting PARALLEL generation for course {course_id} with {course.metadata.total_modules} modules")
            
            # Generate introduction first (quick)
            introduction = await self.claude_service.generate_course_introduction(
                course.metadata,
                course.user_prompt,
                course.user_interests
            )
            await self._update_course_introduction(course_id, introduction)
            
            # 🔥 PARALLEL MODULE GENERATION: Create ALL modules concurrently
            if course.metadata.module_list:
                
                # Create semaphore to limit concurrent Claude API calls (avoid rate limits)
                semaphore = asyncio.Semaphore(3)  # Max 3 concurrent generations
                
                # Create tasks for ALL modules at once
                module_tasks = []
                for module_index in range(len(course.metadata.module_list)):
                    task = self._generate_single_module_with_semaphore(
                        semaphore, course_id, course, module_index
                    )
                    module_tasks.append(task)
                
                logger.info(f"🎯 Launching {len(module_tasks)} module generation tasks in parallel...")
                
                # Execute ALL module generations concurrently
                results = await asyncio.gather(*module_tasks, return_exceptions=True)
                
                # Process results
                successful_modules = []
                failed_modules = []
                
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(f"❌ Module {i+1} generation failed: {str(result)}")
                        failed_modules.append(i+1)
                    elif result is not None:
                        logger.info(f"✅ Module {i+1} generated successfully: {result.title}")
                        successful_modules.append(result)
                    else:
                        logger.warning(f"⚠️ Module {i+1} returned None")
                        failed_modules.append(i+1)
                
                logger.info(f"🎉 Parallel generation completed:")
                logger.info(f"   ✅ Successful: {len(successful_modules)}/{len(module_tasks)} modules")
                logger.info(f"   ❌ Failed: {len(failed_modules)} modules")
                
                if successful_modules:
                    # Mark course as ready with available modules
                    await self._mark_course_ready(course_id)
                    logger.info(f"📚 Course {course_id} marked as ready with {len(successful_modules)} modules")
                else:
                    await self._mark_course_error(course_id, "No modules could be generated")
                    return
            
            # Cache completed course
            await self.cache_service.cache_course(course_id, {"status": "ready"})
            
            logger.info(f"🎯 Course {course_id} PARALLEL generation completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error in parallel course generation: {str(e)}")
            await self._mark_course_error(course_id, str(e))
    
    async def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID with caching - handles null modules during generation"""
        
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
                # Handle null modules during generation - filter them out for validation
                if "modules" in course_doc and course_doc["modules"]:
                    # Filter out null modules for Course validation
                    course_doc["modules"] = [m for m in course_doc["modules"] if m is not None]
                else:
                    course_doc["modules"] = []
                
                course = Course(**course_doc)
                
                # Cache for future requests (only cache when course is ready)
                if course.status == CourseStatus.READY:
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
        """Save module to course in database at the correct position"""
        database = await get_database()
        
        # Extract module index from module_id (e.g., "modulo_2" -> index 1)
        module_index = int(module.module_id.split("_")[1]) - 1
        
        # Use $set to place module at specific position in array
        await database.courses.update_one(
            {"_id": course_id},
            {"$set": {f"modules.{module_index}": module.dict()}}
        )
        
        logger.info(f"✅ Module saved at position {module_index}: {module.title}")
        
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
                
                # Search for relevant videos for the module and individual sections
                module_videos = await self.youtube_service.search_videos_for_module(
                    module_title,
                    module_structure["concepts"],
                    course.user_prompt,
                    module_index=module_index  # ✨ Pass module index for variety
                )
                
                # Search for videos for each section/chunk
                section_videos = []
                for i, chunk in enumerate(chunks):
                    try:
                        # Use the corresponding concept as the title for video search
                        concept_title = module_structure["concepts"][i] if i < len(module_structure["concepts"]) else f"Sección {i+1}"
                        
                        section_video = await self.youtube_service.search_videos_for_concept(
                            concept_title,
                            course.user_prompt,
                            max_results=1,  # One video per section
                            module_index=module_index  # ✨ Pass module index for variety
                        )
                        if section_video:
                            # Add the video to the chunk
                            chunk.video = section_video[0]
                            section_videos.extend(section_video)
                    except Exception as e:
                        logger.warning(f"Error getting video for section {i+1}: {e}")
                        continue
                
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
                for video in module_videos:
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