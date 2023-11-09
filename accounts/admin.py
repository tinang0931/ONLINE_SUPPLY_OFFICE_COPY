from django.contrib import admin
from .models import Item


# Register your models here.
from .models import *  

admin.site.register(Item)

