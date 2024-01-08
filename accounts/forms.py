from django import forms
from .models import Item




class RequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
from .models import request
class requestForm(forms.ModelForm):
    class Meta:
        model = request
        fields = ['status']

