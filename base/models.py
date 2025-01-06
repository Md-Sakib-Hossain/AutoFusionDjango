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


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE) 
    def __str__(self):
        return f"{self.car.make} {self.car.model} for {self.user.username}"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f"{self.quantity} x {self.car.make} {self.car.model} for {self.user.username}"


from django.db import models
from django.conf import settings

class Order(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)  
    card_expiry = models.CharField(max_length=5, null=True, blank=True)
    card_cvv = models.CharField(max_length=3, null=True, blank=True)
    cardholder_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    
    # ForeignKey for the Car model and a quantity field
    car = models.ForeignKey('Car', on_delete=models.CASCADE, null=True)

    quantity = models.PositiveIntegerField(default=0)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

