from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth.models import AbstractUser
import uuid
from decimal import Decimal




class Item(models.Model):
    purpose = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    item_brand_description = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    submission_date = models.DateField(auto_now_add=True)
    request_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, max_length=8)

    @property
    def total_price(self):
        return Decimal(str(self.unit_cost)) * self.quantity









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

# class Item(models.Model):
#     user = 

# class tracker(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     item_name = models.CharField(max_length=100)
#     description = models.TextField()
#     quantity = models.IntegerField()
#     is_submitted = models.BooleanField(default=False)
#     approved = models.BooleanField(default=False)
#     disapproved = models.BooleanField(default=False)
#     budget_officer_approval = models.CharField(max_length=100)
#     campus_director_approval = models.CharField(max_length=100)
#     bac_secretariat_resolution = models.CharField(max_length=100)
#     date_update_status = models.DateField()
#     status = models.CharField(max_length=100)
    

#class CampusDirectorHistoryCD(models.Model):
# user = models.ForeignKey(User, on_delete=models.CASCADE)
# start_date = models.DateField()
# end_date = models.DateField()
# description = models.TextField()
#def __str__(self):
#   return f'Campus Director History: {self.user.username}'

#class SupplyOfficeHistory(models.Model):
#   start_date = models.DateField()
#  end_date = models.DateField()
#  description = models.TextField()
#  def __str__(self):
     #   return f'Supply Office History: {self.start_date} to {self.end_date}'

#class SearchItem(models.Model):
#    title = models.CharField(max_length=200)
#   description = models.TextField()
#  link = models.URLField()
# created_at = models.DateTimeField(default=timezone.now)