import asyncio
import json
import logging
from typing import Optional, Any, Dict, List
import redis.asyncio as redis
import hashlib
from datetime import datetime, timedelta
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class CacheService:
    """Redis-based caching service for optimizing AI responses and expensive operations"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client: Optional[redis.Redis] = None
        
    async def connect(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                self.settings.redis_url,
                encoding='utf-8',
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                max_connections=20
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Successfully connected to Redis")
            
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {str(e)}")
            logger.warning("Running in development mode without cache")
            self.redis_client = None
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")
    
    def _generate_cache_key(self, prefix: str, *args) -> str:
        """Generate a consistent cache key from prefix and arguments"""
        key_data = f"{prefix}:" + ":".join(str(arg) for arg in args)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get_cached_ai_response(
        self, 
        prompt: str, 
        model: str = "claude",
        user_level: str = None,
        interests: List[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get cached AI response for similar prompts"""
        
        if not self.redis_client:
            return None
            
        try:
            # Create cache key based on prompt characteristics
            prompt_hash = hashlib.md5(prompt.lower().encode()).hexdigest()
            interests_str = ",".join(sorted(interests)) if interests else ""
            
            cache_key = self._generate_cache_key(
                "ai_response", 
                model, 
                prompt_hash, 
                user_level or "", 
                interests_str
            )
            
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for AI response: {cache_key}")
                return json.loads(cached_data)
                
        except Exception as e:
            logger.error(f"Error getting cached AI response: {str(e)}")
            
        return None
    
    async def cache_ai_response(
        self, 
        prompt: str,
        response: Dict[str, Any],
        model: str = "claude",
        user_level: str = None,
        interests: List[str] = None,
        ttl: int = None
    ) -> bool:
        """Cache AI response for future use"""
        
        if not self.redis_client:
            return False
            
        try:
            prompt_hash = hashlib.md5(prompt.lower().encode()).hexdigest()
            interests_str = ",".join(sorted(interests)) if interests else ""
            
            cache_key = self._generate_cache_key(
                "ai_response", 
                model, 
                prompt_hash, 
                user_level or "", 
                interests_str
            )
            
            # Add metadata to cached response
            cached_data = {
                "response": response,
                "cached_at": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "model": model,
                "user_level": user_level,
                "interests": interests
            }
            
            ttl = ttl or self.settings.ai_response_cache_ttl
            
            await self.redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(cached_data, default=str)
            )
            
            logger.info(f"Cached AI response: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching AI response: {str(e)}")
            return False
    
    async def get_cached_video_search(
        self, 
        search_query: str, 
        max_results: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """Get cached video search results"""
        
        if not self.redis_client:
            return None
            
        try:
            cache_key = self._generate_cache_key(
                "video_search", 
                search_query.lower(), 
                max_results
            )
            
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for video search: {search_query}")
                return json.loads(cached_data)
                
        except Exception as e:
            logger.error(f"Error getting cached video search: {str(e)}")
            
        return None
    
    async def cache_video_search(
        self, 
        search_query: str, 
        results: List[Dict[str, Any]],
        max_results: int = 5,
        ttl: int = None
    ) -> bool:
        """Cache video search results"""
        
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key(
                "video_search", 
                search_query.lower(), 
                max_results
            )
            
            cached_data = {
                "results": results,
                "cached_at": datetime.utcnow().isoformat(),
                "search_query": search_query,
                "max_results": max_results
            }
            
            ttl = ttl or self.settings.video_search_cache_ttl
            
            await self.redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(cached_data, default=str)
            )
            
            logger.info(f"Cached video search: {search_query}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching video search: {str(e)}")
            return False
    
    async def get_cached_course(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get cached course data"""
        
        if not self.redis_client:
            return None
            
        try:
            cache_key = self._generate_cache_key("course", course_id)
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for course: {course_id}")
                return json.loads(cached_data)
                
        except Exception as e:
            logger.error(f"Error getting cached course: {str(e)}")
            
        return None
    
    async def cache_course(
        self, 
        course_id: str, 
        course_data: Dict[str, Any],
        ttl: int = None
    ) -> bool:
        """Cache course data"""
        
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key("course", course_id)
            
            cached_data = {
                "course": course_data,
                "cached_at": datetime.utcnow().isoformat()
            }
            
            ttl = ttl or self.settings.course_cache_ttl
            
            await self.redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(cached_data, default=str)
            )
            
            logger.info(f"Cached course: {course_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching course: {str(e)}")
            return False
    
    async def invalidate_course_cache(self, course_id: str) -> bool:
        """Invalidate course cache when updated"""
        
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key("course", course_id)
            await self.redis_client.delete(cache_key)
            
            logger.info(f"Invalidated cache for course: {course_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error invalidating course cache: {str(e)}")
            return False
    
    async def cache_module_generation_progress(
        self, 
        course_id: str, 
        module_id: str, 
        progress_data: Dict[str, Any]
    ) -> bool:
        """Cache module generation progress for real-time updates"""
        
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key("module_progress", course_id, module_id)
            
            progress_with_timestamp = {
                **progress_data,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Short TTL for progress data (5 minutes)
            await self.redis_client.setex(
                cache_key, 
                300, 
                json.dumps(progress_with_timestamp, default=str)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error caching module progress: {str(e)}")
            return False
    
    async def get_module_generation_progress(
        self, 
        course_id: str, 
        module_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get module generation progress"""
        
        if not self.redis_client:
            return None
            
        try:
            cache_key = self._generate_cache_key("module_progress", course_id, module_id)
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
                
        except Exception as e:
            logger.error(f"Error getting module progress: {str(e)}")
            
        return None
    
    async def set_rate_limit(
        self, 
        user_id: str, 
        action: str, 
        limit: int, 
        window_seconds: int
    ) -> bool:
        """Set rate limit for user actions"""
        
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key("rate_limit", user_id, action)
            current_count = await self.redis_client.get(cache_key)
            
            if current_count is None:
                # First request in window
                await self.redis_client.setex(cache_key, window_seconds, 1)
                return True
            elif int(current_count) < limit:
                # Within limit
                await self.redis_client.incr(cache_key)
                return True
            else:
                # Rate limit exceeded
                return False
                
        except Exception as e:
            logger.error(f"Error setting rate limit: {str(e)}")
            return False
    
    async def clear_all_cache(self) -> bool:
        """Clear all cache (admin function)"""
        
        if not self.redis_client:
            return False
            
        try:
            await self.redis_client.flushdb()
            logger.info("Cleared all cache")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        if not self.redis_client:
            return {}
            
        try:
            info = await self.redis_client.info()
            
            return {
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses"),
                "hit_rate": (
                    info.get("keyspace_hits", 0) / 
                    max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1)
                ) * 100
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {}


# Global cache service instance
cache_service = CacheService()


async def get_cache_service() -> CacheService:
    """Dependency to get cache service instance"""
    return cache_service


async def init_cache():
    """Initialize cache connection"""
    await cache_service.connect()


async def close_cache():
    """Close cache connection"""
    await cache_service.disconnect() 