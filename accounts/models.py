from django.utils import timezone
from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
import uuid
import random
from bson import ObjectId
from bson import ObjectId




class User(AbstractUser):
    CTU_ID_LENGTH = 10
    username = models.CharField(max_length=12, unique=True, primary_key=True)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    contact1 = models.PositiveIntegerField()
    contact2 = models.PositiveIntegerField()

    USER_TYPES = [

        ('regular', 'Regular User'),
        ('cd', 'Campus Director'),
        ('budget', 'Budget Officer'),
        ('bac', 'BAC'),
    ]

    user_type = models.CharField(max_length=15, choices=USER_TYPES)

    is_admin = models.BooleanField(default=False)
    is_regular = models.BooleanField(default=False)
    is_cd = models.BooleanField(default=False)  
    is_budget = models.BooleanField(default=False)
    is_bac = models.BooleanField(default=False)

    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    @property
    def get_user_type_display(self):
        return dict(self.USER_TYPES).get(self.user_type, 'Unknown')

    def save(self, *args, **kwargs):
    
        self.is_admin = self.user_type == 'admin'
        self.is_regular = self.user_type == 'regular'
        self.is_cd = self.user_type == 'cd'
        self.is_budget = self.user_type == 'budget'
        self.is_bac = self.user_type == 'bac'

        super().save(*args, **kwargs)
    def __str__(self):
        return self.username


class Item(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    submission_date = models.DateField(auto_now_add=True)

class appr_ppmp(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    submission_date = models.DateField(auto_now_add=True)
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
    estimate_budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, default="Pending")
    comment = models.TextField(blank=True, null=True)
      


class PPMP(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
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
    estimate_budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


class PR_Items(models.Model):
    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    submission_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
 

class FileMetadata(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='file_uploads/')

class PR(models.Model):
    metadata = models.ForeignKey(FileMetadata, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    purpose = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    pr_identifier = models.ForeignKey('Pr_identifier', on_delete=models.CASCADE, null=True, blank=True)

class Pr_identifier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True)
    pr_id = models.CharField(max_length=8, unique=True, blank=True, null=True)

    def generate_pr_id(self):
        pr_id = str(uuid.uuid4().int)[:8]
        self.pr_id = pr_id
        self.save()
    



class Checkout(models.Model):

    pr_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateField(default=timezone.now)
    bo_status = models.CharField(max_length=20, default="Pending")
    bo_comment = models.TextField(blank=True, null=True) 
    cd_status = models.CharField(max_length=20, default="Pending")
    cd_comment = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)



    @property
    def combined_id(self):
        random_number = str(random.randint(10000000, 99999999)) 
        return f"{str(self.pr_id)}{random_number}"

    def __str__(self):
        return str(self.pr_id)

    

    
class CheckoutItems(models.Model):
    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True, null=True)
    item_brand_description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
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
    estimate_budget = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


   

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
    