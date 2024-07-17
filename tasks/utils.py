from django.core.cache import cache
from django.conf import settings


def truncate_to_minute(dt):
    return dt.replace(second=0, microsecond=0)

def set_cache(key, data):
    cache.set(key, data, timeout=settings.CACHE_TTL)
