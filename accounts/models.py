from django.utils import timezone
from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
import uuid
import random



class User(AbstractUser):
    CTU_ID_LENGTH = 10

    username = models.CharField(max_length=12, unique=True, primary_key=True)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    contact1 = models.PositiveIntegerField()
    contact2 = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)

    USER_TYPES = [
        ('admin', 'Admin'),
        ('regular', 'Regular User'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def save(self, *args, **kwargs):
        # Perform actions based on user_type before saving
        if self.user_type == 'admin':
            # Do something specific for admin users
            self.is_admin = True
        else:
            # Do something specific for regular users
            self.is_admin = False

        # You can add more custom actions based on user_type here

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Item(models.Model):
    
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



class Checkout(models.Model):
    pr_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    submission_date = models.DateField(default=timezone.now)

    @property
    def combined_id(self):
        random_number = str(random.randint(10000000, 99999999))  # Generates an 8-digit number
        return f"{str(self.pr_id)}_{random_number}"

    def __str__(self):
        return str(self.pr_id)

    
class CheckoutItems(models.Model):
    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
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


