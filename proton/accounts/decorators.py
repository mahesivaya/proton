from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=None, redirect_url='login'):
    """
    Restrict view access to specific user roles.
    Example:
        @role_required(['admin', 'doctor'])
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # If user is not logged in, redirect
            if not request.user.is_authenticated:
                return redirect(redirect_url)

            # If user has no role attribute (non-custom user model)
            if not hasattr(request.user, 'role'):
                raise PermissionDenied("User model has no 'role' attribute")

            # Check role match
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("You are not authorized to view this page.")
        return wrapper
    return decorator
