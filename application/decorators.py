def require_role(*allowed_roles):
    def decorator(func):
        def wrapper(*args,**kwargs):
            role=kwargs.get("role","guest")
            if role not in allowed_roles:
                return {
                    "found": False,
                    "name": None,
                    "email": None,
                    "suggestions": [],
                    "message": f"Access denied. Role '{role}' is not allowed to access this resource.",
                    "authorization": False
                }
            return func(*args,**kwargs)
        return wrapper
    return decorator