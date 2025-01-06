from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from.forms import CarForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, CartItem,Order,Wishlist
from django.contrib import messages
from django.db.models import Q



class Home (generic.TemplateView):
  template_name='home.html'

from django.shortcuts import render
from .models import Car

def home(request):
    cars = Car.objects.all().order_by('-id')[:8] 
    return render(request, 'home.html', {'cars': cars})

@login_required
def userdashboard(request):
    user = request.user  # Get the logged-in user
    orders = Order.objects.filter(user=user).order_by('-id')  # Get all orders by the user, most recent first

    context = {
        'username': user.username,
        'email': user.email,
        'orders': orders,  # Pass the user's orders to the template
    }
    return render(request, 'user/userdashboard.html', context)

def admindashboard(request):
   cars = Car.objects.all().order_by('-id')
   return render(request, 'cars/admindashboard.html',{'cars': cars})

def allcars(request):
   cars = Car.objects.all().order_by('-id')
   return render(request, 'cars/allcars.html',{'cars': cars})

def car_details(request, id):
    car = get_object_or_404(Car, id=id)

    price_range_min = car.price - 1000
    price_range_max = car.price + 3000
    
    recommended_cars = Car.objects.filter(price__gte=price_range_min, price__lte=price_range_max).exclude(id=car.id)[:6]  # Exclude the current car

    context = {
        'car': car,
        'recommended_cars': recommended_cars,
    }
    
    return render(request, 'cars/car_details.html', context)


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

@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, car=car)
    if created:
        messages.success(request, f"{car.make} {car.model} has been added to your wishlist.")
    else:
        messages.info(request, f"{car.make} {car.model} is already in your wishlist.")
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context)

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

###########################order related#############
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        item.total_price = item.car.price * item.quantity  
        total_price += item.total_price  
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }


    return render(request, 'cart/place_order.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, CartItem, Car
from decimal import Decimal
# @login_required


from decimal import Decimal
from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.shortcuts import render, redirect
from .models import Order, CartItem
from decimal import Decimal

def confirm_order(request):
    total_price = Decimal('0.0') 

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('expiry_date')
        card_cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholder_name')

        cart_items = CartItem.objects.filter(user=request.user)

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            card_number=card_number,
            card_expiry=card_expiry,
            card_cvv=card_cvv,
            cardholder_name=cardholder_name,
            status=Order.PENDING
        )

        for cart_item in cart_items:
            car = cart_item.car
            quantity = cart_item.quantity
            item_total_price = car.price * quantity
            total_price += item_total_price

            Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvv=card_cvv,
                cardholder_name=cardholder_name,
                status=Order.PENDING,
                car=car, 
                quantity=quantity,  
                total_price=item_total_price  
            )
            order.total_price = total_price
            order.save()

            car.quantity -= quantity
            car.save()

            cart_item.delete()
        
        return redirect('order_success', order_id=order.id)

    return render(request, 'cart/confirm_order.html', {'total_price': total_price})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/order_success.html', {'order': order})

def manage_orders(request):
    orders = Order.objects.all()  
    context = {
        'orders': orders,
    }
    return render(request, 'cars/manage_orders.html', context)

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.ORDER_STATUS_CHOICES):  # Validate status
            order.status = new_status
            order.save()
            return redirect('manage-orders')
    context = {
        'order': order,
        'status_choices': Order.ORDER_STATUS_CHOICES,
    }
    return render(request, 'cars/update_order_status.html', context)



def car_compare(request):
    # Get the search queries from GET parameters (default to empty strings if not provided)
    search_query_1 = request.GET.get('search_1', '')
    search_query_2 = request.GET.get('search_2', '')

    # Filter cars based on the search queries
    car_1 = None
    car_2 = None

    if search_query_1:
        car_1 = Car.objects.filter(
            Q(make__icontains=search_query_1) |
            Q(model__icontains=search_query_1) |
            Q(description__icontains=search_query_1)
        ).first()  # Get the first car that matches the query (or None if not found)

    if search_query_2:
        car_2 = Car.objects.filter(
            Q(make__icontains=search_query_2) |
            Q(model__icontains=search_query_2) |
            Q(description__icontains=search_query_2)
        ).first()  # Get the first car that matches the query (or None if not found)

    return render(request, 'cars/compare.html', {
        'car_1': car_1,
        'car_2': car_2,
        'search_query_1': search_query_1,
        'search_query_2': search_query_2
    })
    
from django.db.models import Q

def search_page(request):
    query=request.GET.get('query', '')
    results=[]
    if query:
        results=Car.objects.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query)
        )
    return render(request, 'search.html', {'results': results, 'query': query})