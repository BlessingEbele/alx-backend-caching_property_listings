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
