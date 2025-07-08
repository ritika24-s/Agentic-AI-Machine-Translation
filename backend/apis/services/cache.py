import redis
import json
import hashlib
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Redis-based caching for translations"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 3600 * 24  # 24 hours
    
    def _generate_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate consistent cache key"""
        content = f"{text}:{source_lang}:{target_lang}"
        return f"translation:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def get_translation(
        self, 
        text: str, 
        source_language: str, 
        target_language: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached translation"""
        try:
            cache_key = self._generate_cache_key(text, source_language, target_language)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Cache hit for key: {cache_key}")
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set_translation(
        self,
        text: str,
        source_language: str,
        target_language: str,
        translation_data: Dict[str, Any],
        ttl: Optional[int] = None
    ):
        """Cache translation result"""
        try:
            cache_key = self._generate_cache_key(text, source_language, target_language)
            ttl = ttl or self.default_ttl
            
            self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(translation_data)
            )
            
            logger.info(f"Cached translation for key: {cache_key}")
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")