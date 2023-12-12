from django.shortcuts import redirect
from functools import wraps


def unauthenticated_user(view_func):
    """
    Decorator for views that should only be accessible by unauthenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('request')  
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def authenticated_user(view_func):
    """
    Decorator for views that should only be accessible by authenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('bac_home') 
    return _wrapped_view