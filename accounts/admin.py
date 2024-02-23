# admin.py
from django.contrib import admin
from .models import User  # Assuming your model class is named User and it's in the same directory

admin.site.register(User)