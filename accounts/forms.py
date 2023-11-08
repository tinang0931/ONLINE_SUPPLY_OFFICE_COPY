from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['department', 'purpose', 'name', 'description', 'quantity', 'price', 'total_cost']


