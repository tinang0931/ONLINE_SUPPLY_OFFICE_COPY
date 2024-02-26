from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path('', views.landing, name='landing'),
    
]
