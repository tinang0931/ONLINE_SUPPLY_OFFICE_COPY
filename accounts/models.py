from django.db import models



# Create your models here.

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


