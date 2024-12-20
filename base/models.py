from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="car_images/")
    description = models.TextField(blank=True, null=True)  
    quantity = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"




class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f"{self.quantity} x {self.car.make} {self.car.model} for {self.user.username}"
