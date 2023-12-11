from django.utils import timezone
from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver
import uuid
import random
from djongo import models



class User(AbstractUser):
    id = models.ObjectIdField(primary_key=True)
    class Role(models.TextChoices):
        BAC_SECRETARIAT = "BAC SECRETARIAT", "BAC SECRETARIAT"
        REGULAR_USER = "REGULAR USER", "REGULAR USER"
        CAMPUS_DIRECTOR = "CAMPUS_DIRECTOR", "CAMPUS DIRECTOR"
        BUDGET_OFFICER = "BUDGET_OFFICER", "BUDGET OFFICER"

    role = models.CharField(max_length=50, choices=Role.choices)
    base_role = models.CharField(max_length=50, choices=Role.choices)  # Add base_role field

    def save(self, *args, **kwargs):
        if not self.pk:
            self.base_role = self.role  # Set base_role when creating a new user
        return super().save(*args, **kwargs)
        

class BAC_SECRETARIAT(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.BAC_SECRETARIAT)
class BAC_SECRETARIAT(User):
    base_role = User.Role.BAC_SECRETARIAT
    Bac = BAC_SECRETARIAT()
    class Meta:
        proxy = True
    def welcome(self):
        return "Only for Bac Secretariats"

@receiver(post_save, sender=BAC_SECRETARIAT)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BAC_SECRETARIAT":
        BAC_SECRETARIAT.Profile.objects.create(user=instance)
class BAC_SECRETARIAT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ctu_id = models.IntegerField(null=True, blank=True)

    



class RegularUser(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.request)
class Regular(User):
    base_role = User.Role.REGULAR_USER
    Regular = RegularUser()
    class Meta:
        proxy = True
    def welcome(self):
        return "Only for Requesters"

@receiver(post_save, sender=Regular)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "Regular":
        Regular.Profile.objects.create(user=instance)
class RegularProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ctu_id = models.IntegerField(null=True, blank=True)




class CAMPUS_DIRECTOR(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CAMPUS_DIRECTOR)
class CAMPUS_DIRECTOR(User):
    base_role = User.Role.CAMPUS_DIRECTOR
    Campus = CAMPUS_DIRECTOR()
    class Meta:
        proxy = True
    def welcome(self):
        return "Only for Campus Directors"
class CAMPUS_DIRECTOR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ctu_id = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=CAMPUS_DIRECTOR)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CAMPUS_DIRECTOR":
        CAMPUS_DIRECTOR.objects.create(user=instance)



class BudgetManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.bohome)
class Budget(User):
    base_role = User.Role.BUDGET_OFFICER
    Budget = BudgetManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Budget Officers"
class BudgetProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ctu_id = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=Budget)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BUDGET OFFICER":
        BudgetProfile.objects.create(user=instance)


def base_role(self):
        return determine_base_role(self.user_type)

def determine_base_role(user_type):
    if user_type == 'BAC Secretariat':
        return User.Role.BAC_SECRETARIAT
    elif user_type == 'Campus Director':
        return User.Role.CAMPUS_DIRECTOR
    elif user_type == 'Budget Officer':
        return User.Role.BUDGET_OFFICER
    elif user_type == 'Regular User':
        return User.Role.REGULAR_USER
    else:
        return None  # or any other default value, or handle the invalid case appropriately
        

class Item(models.Model):
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)
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
    pr_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    submission_date = models.DateField(default=timezone.now)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    date_updated = models.DateField(auto_now=True)
    

    # ... other fields and methods ...


    @property
    def combined_id(self):
        random_number = str(random.randint(10000000, 99999999))  # Generates an 8-digit number
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

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Add total_cost field

    def save(self, *args, **kwargs):
        # Calculate total_cost before saving
        self.total_cost = self.unit_cost * self.quantity
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    pr_id = models.CharField(max_length=50)  # Add pr_id field

    def __str__(self):
        return f"Comment by {self.pr_id} at {self.timestamp}"
    

class CsvFile(models.Model):
    CATEGORY = models.CharField(max_length=255)
    ITEM_BRAND = models.CharField(max_length=255)
    ITEMS = models.CharField(max_length=255)
    UNIT = models.CharField(max_length=50)
    PRICE = models.DecimalField(max_digits=10, decimal_places=2)


class Bac_Item(models.Model):
    Category = models.CharField(max_length=255)
    Item_Brand  = models.CharField(max_length=255)
    Item_name = models.CharField(max_length=255)
    Unit = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=10, decimal_places=2)

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