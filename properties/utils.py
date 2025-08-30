# properties/utils.py
from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetch all properties with Redis caching.
    Cache key: 'all_properties'
    Expiry: 1 hour (3600 seconds)
    """
    properties = cache.get("all_properties")
    if not properties:
        properties = list(Property.objects.all().values("id", "title", "description", "price"))
        cache.set("all_properties", properties, 3600)  # 1 hour
    return properties


import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        # Log metrics as required
        logger.error(f"Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis cache metrics: {e}")
        return {}
