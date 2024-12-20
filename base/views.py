from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from.forms import CarForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, CartItem
from django.contrib import messages



class Home (generic.TemplateView):
  template_name='home.html'

from django.shortcuts import render
from .models import Car

def home(request):
    cars = Car.objects.all().order_by('-id')[:8] 
    return render(request, 'home.html', {'cars': cars})

def admindashboard(request):
   cars = Car.objects.all().order_by('-id')
   return render(request, 'cars/admindashboard.html',{'cars': cars})

def allcars(request):
   cars = Car.objects.all().order_by('-id')
   return render(request, 'cars/allcars.html',{'cars': cars})

def car_details(request, id):
    car = get_object_or_404(Car, id=id)
    return render(request, 'cars/car_details.html', {'car': car})


#Car update,delete,edit

def createcar(request):
    form = CarForm()  
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  
    return render(request, 'cars/car_form.html', {'form': form})



def updatecar(request, id):
    car = get_object_or_404(Car, id=id)  
    form = CarForm(request.POST or None, request.FILES or None, instance=car)  
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard') 

    return render(request, 'cars/car_form.html', {'form': form})



def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    
    if request.method == 'POST':
        car.delete()  
        return redirect('admin_dashboard')  
    return render(request)


#Cart Funcionality

@login_required
def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, car=car)
    if created:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('cart')



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        item.total_price = item.car.price * item.quantity  
        total_price += item.total_price  
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)

def update_cart(request, item_id):
    if request.method == "POST":
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)
        available_quantity = cart_item.car.quantity 
        if action == "increase":
            if cart_item.quantity < available_quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, "Cannot add more. Only {} items available.".format(available_quantity))
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        return redirect('cart')  


def delete_item(request, item_id):
    if request.method == "POST":
        cart_item = CartItem.objects.get(id=item_id)  
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect('cart')  
