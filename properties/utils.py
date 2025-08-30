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


# properties/utils.py
from django.core.cache import cache
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    queryset = cache.get('all_properties')
    if not queryset:
        from .models import Property
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)
    return queryset


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics
