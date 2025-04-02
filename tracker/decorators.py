from django.shortcuts import render
from functools import wraps

def require_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "tracker/auth_required.html", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
