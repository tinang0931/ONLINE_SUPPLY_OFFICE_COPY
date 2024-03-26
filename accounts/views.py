
from django.shortcuts import render
from .config import CAMPUS_NAME, SITE_TITLE, HEADING_TEXT, SUBHEADING_TEXT

def landing(request):
    return render(request, 'accounts/User/landing.html')
def userlanding(request):
    context = {
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT
    }
    return render(request, 'accounts/User/userlanding.html', context)

def login(request):
    return render(request, 'accounts/User/login.html')

def reset_password(request):
    return render(request, 'accounts/User/reset_password.html')

def logout_user(request):
    pass

def register(request):
    return render(request, 'accounts/User/register.html')

def ppmp101(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/ppmp101.html', context)

def purchase (request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/purchase.html', context)

def tracker(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/tracker.html', context)

def purchasetracker(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/purchasetracker.html', context)

def about(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/about.html', context)

def ppmp(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/ppmp.html', context)

def catalogue(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/catalogue.html', context )

def user_add_new_item(request):
    return render(request, 'accounts/User/ppmp.html')

def approved_ppmp(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/approved_ppmp.html', context)