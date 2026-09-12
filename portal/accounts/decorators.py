from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def staff_required(view_func):
    # like login_required, but 403s non-admins instead of redirecting them
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied('Admin access only.')
        return view_func(request, *args, **kwargs)

    return _wrapped
