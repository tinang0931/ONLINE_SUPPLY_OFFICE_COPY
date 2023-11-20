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


class PurchaseRequest(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    submission_date = models.DateField()
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()
    # Add other fields as needed

    def calculate_total_cost(self):
        # Add your logic to calculate the total cost
        return self.quantity * self.unit_cost  # Adjust this according to your actual calculation

    total_cost = property(calculate_total_cost)