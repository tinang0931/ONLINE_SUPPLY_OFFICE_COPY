from django.db import models
from django.contrib.auth.models import  User

# class User(AbstractUser):
#     is_admin = models.BooleanField(default= False)
#     is_regularuser = models.BooleanField(default= False)

class Department(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    item_number = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    unit = models.CharField(max_length=255)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name  # Customize this to display the item name or number

class Purpose(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description



class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'Transaction by {self.user.username} at {self.timestamp}'



class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Code: {self.code} for {self.email}'

