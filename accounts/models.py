from django.db import models
from django.template import RequestContext


class Requester (models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self)   :
        return self.name
    
class Tag (models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self)   :
        return self.name

class Products(models.Model):

    CATEGORY = (
    ('Sports', 'Sports'),
    ('Laboratory', 'Laboratory')
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True, choices=CATEGORY)
    description = models.CharField(max_length=200,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self)   :
        return self.name


class Status(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )

    requester = models.ForeignKey(Requester, null=True, on_delete=models.SET_NULL)
    products = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)      
    status = models.CharField(max_length=200,null=True, choices=STATUS)


from django.db import models
from django.contrib.auth.models import User 


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=255)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=255)
    purpose = models.TextField()
    
    # Add a user_id field to store the user's identifier for the request
    user_id = models.CharField(max_length=10, unique=True, blank=True, null=True)  # Adjust the max_length as needed

    # ... other fields ...

    def save(self, *args, **kwargs):
        # Generate a unique user_id for the request
        if not self.user_id:
            self.user_id = self.generate_unique_user_id()
        super().save(*args, **kwargs)

    def generate_unique_user_id(self):
        # Implement your logic to generate a unique user_id here
        # Example: Generate a random alphanumeric user_id
        # Make sure it's unique in your system
        import random
        import string

        while True:
            user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Item.objects.filter(user_id=user_id).exists():
                return user_id

    # ... other methods ...

    def __str__(self):
        return self.name



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


