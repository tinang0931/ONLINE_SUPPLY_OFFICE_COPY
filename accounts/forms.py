from django import forms
from .models import Document, Item
from .models import User
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404




class RequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'contact1', 'contact2', 'email', 'user_type')
