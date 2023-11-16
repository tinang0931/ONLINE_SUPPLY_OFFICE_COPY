from django import forms
from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
import uuid


class Item(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField(default=1)
    submission_date = models.DateField(auto_now_add=True)

    @property
    def total_cost(self):
        return Decimal(str(self.unit_cost)) * self.quantity
    
    
    




class CsvFile(models.Model):
    CATEGORY = models.CharField(max_length=255)
    ITEM_BRAND = models.CharField(max_length=255)
    ITEMS = models.CharField(max_length=255)
    UNIT = models.CharField(max_length=50)
    PRICE = models.DecimalField(max_digits=10, decimal_places=2)

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Code: {self.code} for {self.email}'

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_request_id = models.CharField(max_length=20)
    date_requested = models.DateField()
    purpose = models.CharField(max_length=200)
    quantity = models.IntegerField()
    status_description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
  


    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
    

class PurchaseRequestForm(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     item_name = models.CharField(max_length=100)
     description = models.TextField()
     quantity = models.IntegerField()
     is_submitted = models.BooleanField(default=False)
     approved = models.BooleanField(default=False)
     disapproved = models.BooleanField(default=False)

    
def __str__(self):
         return self.item_name


class User(AbstractUser):
    # Add your additional fields here

    # Define the 'groups' and 'user_permissions' fields with a 'related_name'
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='accounts_user_set',   # Add this line
        related_query_name='accounts_user', # Add this line
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',   # Add this line
        related_query_name='accounts_user', # Add this line

    )
    
