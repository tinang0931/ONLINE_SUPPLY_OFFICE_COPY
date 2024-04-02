from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden


def unauthenticated_user(view_func):
    """
    Decorator for views that should only be accessible by unauthenticated users.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('myppmp')  
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

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator
regular_user_required = user_type_required('regular')
budget_required = user_type_required('budget')
bac_required = user_type_required('bac')
cd_required = user_type_required('cd')
admin_required = user_type_required('admin')
