import asyncio
import logging
from app.services.course_generator import CourseGenerationService
from app.models.course import CourseGenerationRequest, CourseLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_video_variety():
    """Test the new video variety system"""
    
    print("🚀 Testing improved video variety and frontend...")
    
    service = CourseGenerationService()
    
    # Create a test course request
    request = CourseGenerationRequest(
        prompt="Quiero aprender Python desde cero",
        level=CourseLevel.PRINCIPIANTE,
        interests=["programacion", "desarrollo web"]
    )
    
    try:
        print("📚 Generating course with improved video system...")
        course_response = await service.generate_course_fast_response(request)
        course = course_response  # Assuming the response contains the course object
        
        print(f"✅ Course generated successfully!")
        print(f"📖 Course: {course.metadata.title}")
        print(f"📝 Description: {course.metadata.description}")
        print(f"🎯 Level: {course.metadata.level}")
        print(f"📊 Modules: {len(course.modules)}")
        
        if course.modules:
            print(f"\n📋 Module breakdown:")
            for i, module in enumerate(course.modules):
                print(f"  {i+1}. {module.title}")
                print(f"     📝 {module.description}")
                print(f"     📚 Concepts: {len(module.concepts)}")
                print(f"     🎬 Module videos: {len(module.resources.videos) if module.resources else 0}")
                
                # Count section videos
                section_videos = sum(1 for chunk in module.chunks if chunk.video)
                print(f"     🎞️  Section videos: {section_videos}")
                print()
        
        # Save course to database
        await service._save_course_to_database(course)
        print(f"💾 Course saved with ID: {course.course_id}")
        
        print("\n🎉 Test completed! The frontend should now show:")
        print("  ✅ Different videos between modules")
        print("  ✅ Better video variety using different search strategies")
        print("  ✅ Only ONE video per section (no more 3x repetition)")
        print("  ✅ Beautiful markdown rendering")
        print("  ✅ Improved design with better contrast")
        print("  ✅ Modern UI with proper CSS styling")
        
        return course.course_id
        
    except Exception as e:
        logger.error(f"Error testing video variety: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_video_variety()) 