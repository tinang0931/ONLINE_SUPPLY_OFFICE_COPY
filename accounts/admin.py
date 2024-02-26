from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserAdmin(UserAdmin):
    # Your customizations here

    admin.site.unregister(User)  # Unregister the default UserAdmin
    admin.site.register(User, UserAdmin)  # Register your custom UserAdmin

