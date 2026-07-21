import functools
import time


def require_role(*allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            role = kwargs.get("role", "guest")
            if role not in allowed_roles:
                return {
                    "found": False,
                    "name": None,
                    "email": None,
                    "suggestions": [],
                    "message": f"Access denied. Role '{role}' is not allowed to access this resource.",
                    "authorization": False,
                }
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _make_cache_key(args, kwargs):
    if kwargs:
        return args + tuple(sorted(kwargs.items()))
    return args


def cached(ttl_seconds: int = 300, maxsize: int = 128):
    def decorator(func):
        cache = {}
        order = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_cache_key(args, kwargs)
            now = time.time()

            if key in cache:
                value, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    if key in order:
                        order.remove(key)
                    order.append(key)
                    return value
                del cache[key]
                if key in order:
                    order.remove(key)

            result = func(*args, **kwargs)
            cache[key] = (result, now)
            order.append(key)
            if len(order) > maxsize:
                oldest = order.pop(0)
                cache.pop(oldest, None)
            return result

        def cache_clear():
            cache.clear()
            order.clear()

        wrapper.cache_clear = cache_clear
        wrapper.cache_info = lambda: {
            "maxsize": maxsize,
            "current_size": len(cache),
            "ttl_seconds": ttl_seconds,
        }
        return wrapper
    return decorator
