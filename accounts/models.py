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

    is_admin = models.BooleanField(default=False) 
    def save(self, *args, **kwargs):
        self.is_admin = self.user_type == 'admin'
        super().save(*args, **kwargs)
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def save(self, *args, **kwargs):
        if self.user_type == 'admin':
            self.is_admin = True
        else:
            self.is_admin = False

        super().save(*args, **kwargs)
    def __str__(self):
        return self.username


class Item(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField()
    submission_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    jan = models.IntegerField(default=0)
    feb = models.IntegerField(default=0)
    mar = models.IntegerField(default=0)
    apr = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    jun = models.IntegerField(default=0)
    jul = models.IntegerField(default=0)
    aug = models.IntegerField(default=0)
    sep = models.IntegerField(default=0)
    oct = models.IntegerField(default=0)
    nov = models.IntegerField(default=0)
    dec = models.IntegerField(default=0)
    mode_of_procurement = models.CharField(max_length=255, blank=True, null=True)
    estimate_budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))





class Checkout(models.Model):
    pr_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    submission_date = models.DateField(default=timezone.now)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    date_updated = models.DateField(auto_now=True)


    @property
    def combined_id(self):
        random_number = str(random.randint(10000000, 99999999)) 
        return f"{str(self.pr_id)}_{random_number}"

    def __str__(self):
        return str(self.pr_id)

    
class CheckoutItems(models.Model):
    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField(default=1)
    submission_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.unit_cost * self.quantity
        super().save(*args, **kwargs)
        

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    pr_id = models.CharField(max_length=50)  
    def __str__(self):
        return f"Comment by {self.pr_id} at {self.timestamp}"
    

class CSV(models.Model):
    id = models.AutoField(primary_key=True)
    Category = models.CharField(max_length=255)
    Item_name = models.CharField(max_length=255)
    Item_Brand = models.CharField(max_length=255)
    Unit = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


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
    def calculate_total_cost(self):
        return self.quantity * self.unit_cost  
    total_cost = property(calculate_total_cost)