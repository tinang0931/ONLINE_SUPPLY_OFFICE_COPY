from django.contrib import admin

# Register your models here.
from .models import *  

admin.site.register(Requester)
admin.site.register(Products)
admin.site.register(Tag)
admin.site.register(Status) 