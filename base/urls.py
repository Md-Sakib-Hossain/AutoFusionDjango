from django.urls import path
from .views import(
  Home
)
urlpatterns = [
  path('',Home.as_view(),name='home'),
    
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL for the main home page
    path('admin-dashboard/', views.admindashboard, name='admin_dashboard'),
    path('allcars/', views.allcars, name='allcars'),
    path('car/<int:id>/', views.car_details, name='car_details'),
    path('create-car/', views.createcar, name='create-car'),
    path('update-car/<int:id>/', views.updatecar, name='update-car'),
    path('delete-car/<int:id>/', views.delete_car, name='delete-car'),
    path('add_to_cart/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart,name='update_cart'),  
    path('cart/delete/<int:item_id>/', views.delete_item,name='delete_item'),  


]


