from django import forms
from .models import Item
from .models import User





class RequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'contact1', 'contact2', 'email', 'user_type')

