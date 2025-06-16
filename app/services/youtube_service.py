import logging
import aiohttp
import asyncio
from typing import List, Optional, Dict, Any
from ..models.course import VideoResource
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for searching YouTube videos with real API integration"""
    
    def __init__(self):
        settings = get_settings()
        self.api_key = getattr(settings, 'youtube_data_api_key', None)
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        
    async def search_videos_for_concept(
        self, 
        concept: str, 
        course_topic: str,
        max_results: int = 2,
        language: str = "es",
        module_index: int = 0  # ✨ NEW: Add module index for variety
    ) -> List[VideoResource]:
        """Search for relevant educational videos for a specific concept with improved variety"""
        
        # 🎯 IMPROVED: Better search strategy with variety based on module
        main_topic = self._extract_main_topic(course_topic)
        
        # 🔄 Add variety by alternating search strategies per module
        search_strategies = [
            f"{main_topic} {concept} tutorial",
            f"{concept} {main_topic} explicacion",
            f"como {concept} {main_topic}",
            f"{main_topic} {concept} ejemplo",
            f"curso {main_topic} {concept}"
        ]
        
        # Use different strategy based on module index
        strategy_index = module_index % len(search_strategies)
        search_query = search_strategies[strategy_index]
        
        # Add "programacion" for better context
        search_query += " programacion"
        
        try:
            videos = await self._search_youtube_videos(
                query=search_query,
                max_results=max_results,
                language=language,
                order="relevance"
            )
            
            # 🔍 Filter videos to ensure they're actually relevant
            filtered_videos = self._filter_relevant_videos(videos, concept, main_topic)
            
            logger.info(f"Found {len(filtered_videos)} relevant videos for concept: {concept} (strategy {strategy_index})")
            return filtered_videos
            
        except Exception as e:
            logger.error(f"Error searching videos for concept {concept}: {str(e)}")
            # Return fallback videos if API fails
            return self._get_fallback_videos(concept, course_topic)
    
    async def search_videos_for_module(
        self, 
        module_title: str,
        concepts: List[str],
        course_topic: str,
        max_results: int = 1,  # ✨ REDUCED: Only 1 module video to avoid clutter
        language: str = "es",
        module_index: int = 0  # ✨ NEW: Add module index for variety
    ) -> List[VideoResource]:
        """Search for videos covering an entire module with better targeting and variety"""
        
        main_topic = self._extract_main_topic(course_topic)
        
        # 🔄 Different search approaches per module
        module_strategies = [
            f"{main_topic} {module_title} tutorial completo",
            f"curso {main_topic} {module_title}",
            f"{module_title} {main_topic} explicacion",
            f"aprende {main_topic} {module_title}"
        ]
        
        strategy_index = module_index % len(module_strategies)
        search_query = module_strategies[strategy_index]
        
        try:
            videos = await self._search_youtube_videos(
                query=search_query,
                max_results=max_results,
                language=language,
                order="relevance"
            )
            
            # Filter for educational content
            filtered_videos = self._filter_educational_videos(videos, module_title, main_topic)
            
            logger.info(f"Found {len(filtered_videos)} videos for module: {module_title} (strategy {strategy_index})")
            return filtered_videos
            
        except Exception as e:
            logger.error(f"Error searching videos for module {module_title}: {str(e)}")
            return self._get_fallback_videos(module_title, course_topic)
    
    def _extract_main_topic(self, course_topic: str) -> str:
        """Extract the main programming language or technology from course topic"""
        
        topic_lower = course_topic.lower()
        
        # Programming languages
        if "python" in topic_lower:
            return "Python"
        elif "javascript" in topic_lower or "js" in topic_lower:
            return "JavaScript"
        elif "java" in topic_lower and "script" not in topic_lower:
            return "Java"
        elif "c++" in topic_lower or "cpp" in topic_lower:
            return "C++"
        elif "c#" in topic_lower or "csharp" in topic_lower:
            return "C#"
        elif "html" in topic_lower:
            return "HTML"
        elif "css" in topic_lower:
            return "CSS"
        elif "react" in topic_lower:
            return "React"
        elif "vue" in topic_lower:
            return "Vue.js"
        elif "angular" in topic_lower:
            return "Angular"
        elif "node" in topic_lower:
            return "Node.js"
        elif "sql" in topic_lower:
            return "SQL"
        elif "web" in topic_lower:
            return "Desarrollo Web"
        elif "programacion" in topic_lower or "programming" in topic_lower:
            return "Programación"
        else:
            return "Programación"
    
    def _filter_relevant_videos(self, videos: List[VideoResource], concept: str, main_topic: str) -> List[VideoResource]:
        """Filter videos to ensure they're relevant to programming/education"""
        
        relevant_videos = []
        
        # Keywords that indicate educational programming content
        educational_keywords = [
            "tutorial", "curso", "aprende", "programacion", "codigo", "desarrollo",
            "tutorial", "course", "learn", "programming", "code", "development",
            "explicacion", "example", "practica", "ejercicio", "proyecto"
        ]
        
        # Keywords to avoid (non-programming contexts)
        avoid_keywords = [
            "clase escolar", "profesor", "estudiantes", "escuela", "colegio",
            "teacher", "school", "classroom", "education system", "music", "song"
        ]
        
        for video in videos:
            title_lower = video.title.lower()
            desc_lower = video.description.lower()
            
            # Check if it contains educational programming keywords
            has_educational = any(keyword in title_lower or keyword in desc_lower 
                                for keyword in educational_keywords)
            
            # Check if it contains main topic
            has_topic = main_topic.lower() in title_lower or main_topic.lower() in desc_lower
            
            # Check if it contains avoid keywords
            has_avoid = any(keyword in title_lower or keyword in desc_lower 
                          for keyword in avoid_keywords)
            
            # Include if it's educational and doesn't have avoid keywords
            if (has_educational or has_topic) and not has_avoid:
                relevant_videos.append(video)
        
        return relevant_videos
    
    def _filter_educational_videos(self, videos: List[VideoResource], module_title: str, main_topic: str) -> List[VideoResource]:
        """Filter videos specifically for educational content"""
        
        educational_videos = []
        
        for video in videos:
            title_lower = video.title.lower()
            
            # Prefer videos with educational indicators
            if any(word in title_lower for word in ["tutorial", "curso", "aprende", "programacion"]):
                educational_videos.append(video)
            elif main_topic.lower() in title_lower:
                educational_videos.append(video)
        
        return educational_videos[:2]  # Return top 2 most relevant
    
    async def _search_youtube_videos(
        self,
        query: str,
        max_results: int = 3,
        language: str = "es",
        order: str = "relevance"
    ) -> List[VideoResource]:
        """Perform actual YouTube API search with better filtering"""
        
        if not self.api_key:
            logger.warning("YouTube API key not configured, using fallback videos")
            return self._get_fallback_videos(query, "")
        
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results * 3,  # Search more to filter better
            "order": order,
            "relevanceLanguage": language,
            "regionCode": "ES" if language == "es" else "US",
            "videoDuration": "medium",  # Prefer medium length videos (4-20 min)
            "videoDefinition": "high",
            "videoCategoryId": "27",  # Education category
            "key": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        videos = []
                        
                        for item in data.get("items", []):
                            try:
                                video = VideoResource(
                                    video_id=item["id"]["videoId"],
                                    title=item["snippet"]["title"],
                                    description=item["snippet"]["description"][:300] + "..." if len(item["snippet"]["description"]) > 300 else item["snippet"]["description"],
                                    thumbnail_url=item["snippet"]["thumbnails"]["medium"]["url"],
                                    channel_name=item["snippet"]["channelTitle"],
                                    duration="",  # Would need additional API call
                                    url=f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                                )
                                videos.append(video)
                                
                                if len(videos) >= max_results:
                                    break
                                    
                            except Exception as e:
                                logger.warning(f"Error parsing video item: {e}")
                                continue
                        
                        return videos
                    else:
                        logger.error(f"YouTube API error: {response.status}")
                        return self._get_fallback_videos(query, "")
                        
        except Exception as e:
            logger.error(f"Error calling YouTube API: {str(e)}")
            return self._get_fallback_videos(query, "")
    
    def _get_fallback_videos(self, topic: str, course_topic: str) -> List[VideoResource]:
        """Generate fallback videos when API is not available"""
        
        # Create realistic fallback videos based on topic
        fallback_videos = []
        main_topic = self._extract_main_topic(course_topic) if course_topic else "Programación"
        
        # Generic educational channels for different topics
        if "python" in topic.lower() or "Python" in main_topic:
            fallback_videos = [
                VideoResource(
                    video_id="kqtD5dpn9C8",
                    title=f"Python Tutorial - {topic}",
                    description=f"Tutorial completo sobre {topic} en Python con ejemplos prácticos.",
                    thumbnail_url="https://img.youtube.com/vi/kqtD5dpn9C8/mqdefault.jpg",
                    channel_name="Programación ATS",
                    duration="15:30",
                    url="https://www.youtube.com/watch?v=kqtD5dpn9C8"
                )
            ]
        elif "javascript" in topic.lower() or "JavaScript" in main_topic:
            fallback_videos = [
                VideoResource(
                    video_id="DLikpfc64cA",
                    title=f"JavaScript Tutorial - {topic}",
                    description=f"Aprende {topic} en JavaScript paso a paso.",
                    thumbnail_url="https://img.youtube.com/vi/DLikpfc64cA/mqdefault.jpg",
                    channel_name="MoureDev",
                    duration="20:45",
                    url="https://www.youtube.com/watch?v=DLikpfc64cA"
                )
            ]
        else:
            # Generic fallback for other topics
            fallback_videos = [
                VideoResource(
                    video_id="placeholder1",
                    title=f"{main_topic} - {topic}",
                    description=f"Aprende {topic} en {main_topic} de manera práctica.",
                    thumbnail_url="https://img.youtube.com/vi/placeholder1/mqdefault.jpg",
                    channel_name="Canal Educativo",
                    duration="12:30",
                    url="https://www.youtube.com/watch?v=placeholder1"
                )
            ]
        
        return fallback_videos[:1]  # Return only 1 fallback video to avoid clutter