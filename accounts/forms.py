from django import forms
from .models import Item

class RequestItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        
             
     
# class tracker(forms.ModelForm):
    
#     class Meta:
#         model = Item
#         fields = '__all__'