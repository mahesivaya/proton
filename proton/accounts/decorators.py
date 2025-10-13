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

    def decorator(view_func, unauthorized_view='unauthorized'):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # If user is not logged in, redirect
            if not request.user.is_authenticated:
                return redirect(unauthorized_view)

            # If user has no role attribute (non-custom user model)
            if not hasattr(request.user, 'role'):
                return redirect(unauthorized_view)

            # Check role match
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(unauthorized_view)
        return wrapper
    return decorator
