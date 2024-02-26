from django.shortcuts import render
from .models import *

def landing(request):
    return render(request, 'accounts/User/landing.html')


def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    contact1 = request.POST.get('contact1')
    
    
    user = User(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        contact1=contact1,
        
    )
    
    user.save()
    return render(request, 'accounts/User/register.html')