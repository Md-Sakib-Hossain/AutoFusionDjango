from django.contrib import admin

from .models import Car,CartItem,Order,Wishlist


admin.site.register(Car)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Wishlist)
