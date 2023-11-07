from django import forms
from .models import Item


class RequesterForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_description', 'unit', 'unit_cost', 'quantity', 'total_cost']

