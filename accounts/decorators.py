from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden


def unauthenticated_user(view_func):
    """
    Decorator for views that should only be accessible by unauthenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('ppmp')  
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



def regular_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'regular':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")

    return _wrapped_view
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")

    return _wrapped_view