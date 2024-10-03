from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, default='user')

class Inbound(models.Model):
    
    ref = models.CharField(max_length=100, unique=True, blank=True)
    date = models.DateField()
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='pending')
    
    def __str__(self):
        return f"Inbound {self.ref} - {self.sku}"


class Outbound(models.Model):
   
    ref = models.CharField(max_length=100, unique=True, blank=True)  
    date = models.DateField()
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='shipped')
    
    def __str__(self):
        return f"Outbound {self.ref} - {self.sku}"
    
class Inventory(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Inventory {self.sku} - {self.name}"