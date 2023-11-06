from django import forms
from .models import Item

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('_all_')  # You can specify the fields you want to include
