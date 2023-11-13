from django import forms
from .models import Item

class RequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
class YourModelForm(forms.ModelForm):
    class Meta:
        model = RequestItemForm
        fields = '__all__'