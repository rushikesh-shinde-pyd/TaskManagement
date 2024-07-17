# Django imports
from django.core.cache import cache
from django.conf import settings


def truncate_to_minute(dt):
    """
    Truncates datetime object `dt` to the nearest minute by setting seconds and microseconds to zero.
    """
    return dt.replace(second=0, microsecond=0)


def set_cache(key, data):
    """
    Sets `data` in Django cache with specified `key` and timeout from settings.
    """
    cache.set(key, data, timeout=settings.CACHE_TTL)
