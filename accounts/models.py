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
