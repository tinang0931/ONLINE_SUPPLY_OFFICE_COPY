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
    status = models.CharField(max_length=20)
    status_description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
  


    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
    
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
   # description = models.TextField()

    #def __str__(self):
     #   return f'Supply Office History: {self.start_date} to {self.end_date}'

#class SearchItem(models.Model):
#    title = models.CharField(max_length=200)
 #   description = models.TextField()
  #  link = models.URLField()
   # created_at = models.DateTimeField(default=timezone.now)


class PurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    approved = models.BooleanField(default=False)
    disapproved = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name
