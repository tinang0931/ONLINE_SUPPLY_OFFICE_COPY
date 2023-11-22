from django.shortcuts import redirect
from functools import wraps


def unauthenticated_user(view_func):
    """
    Decorator for views that should only be accessible by unauthenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('request')  # Redirect to the home page if the user is already authenticated
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def authenticated_user(view_func):
    """
    Decorator for views that should only be accessible by authenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to the login page if the user is not authenticated
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('login')  # You can change 'login' to the appropriate login URL
        return view_func(request, *args, **kwargs)

    return wrapper
def regular_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_regular:
            return redirect('login')  # You can change 'login' to the appropriate login URL
        return view_func(request, *args, **kwargs)

    return wrapper