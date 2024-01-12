from django import forms
from .models import Item
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
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'contact1', 
            'contact2', 
            'email', 
            'user_type'
        )
        
        widgets = {
            'username': forms.NumberInput(attrs={'placeholder': 'CTUID'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'contact1': forms.TextInput(attrs={'placeholder': 'Contact No.'}),
            'contact2': forms.TextInput(attrs={'placeholder': 'Contact No.'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Add'}),
            'user_type': forms.Select(
                choices=[
                    ('admin', 'Admin'),
                    ('regular', 'Regular User'),
                    ('cd', 'Campus Director'),
                    ('budget', 'Budget Officer'),
                    ('bac', 'BAC'),
                ],
                attrs={'placeholder': 'User Type'},
            ),
        }
