from django.shortcuts import render
from .models import ServiceList

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.core.mail import send_mail

from django.conf import settings

from django.shortcuts import render, redirect
from .models import Service

# Create your views here.
def car_service(request):
    return render(request,"car_service.html")

def appointment(request):
    data = Service.objects.all()
    return render(request,"appointment.html",{"data": data})

def servicelist(request):
    
    data = Service.objects.all()
    return render(request, "servicelist.html", {"data": data})


def adminservice(request):
    data = ServiceList.objects.all()
    context = {"data": data}
    return render(request, "adminservice.html", context)

def manageservice(request):
    data = Service.objects.all()
    return render(request, "manageservice.html", {"data": data})

def insertData(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        service = request.POST.get('service')
        date = request.POST.get('date')
        print(name, email, service, date)
        
        # Save data to the database
        query = ServiceList(name=name, email=email, service=service, date=date)
        query.save()
        
    return render(request, "appointment.html")



def insertservice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Ensure image is fetched from FILES
        learn = request.POST.get('learn')
        query = Service(title=title, description=description, image=image, learn=learn)
        query.save()
        
    
    return render(request, "manageservice.html")


def manage_services(request):
    data = ServiceList.objects.all()
    return render(request, 'adminservice.html', {'data': data})

# def mark_service_arrived(request, service_id):
#     service = get_object_or_404(ServiceList, id=service_id)
#     service.status = 'Arrived'
#     service.save()
#     return redirect('adminservice')
def mark_service_arrived(request, service_id):
    service=get_object_or_404(ServiceList,id=service_id)
    service.a_status='Arrived'
    service.save()
    return redirect('adminservice')

def mark_service_done(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        email_subject = request.POST.get('email_subject')
        email_body = request.POST.get('email_body')

        service = get_object_or_404(ServiceList, id=service_id)
        service.status = 'Done'
        service.save()

        # Send Email to User
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[service.email],
            fail_silently=False,
        )

        return redirect('adminservice')
# def mark_service_done(request, id):
#     service = get_object_or_404(ServiceList, id=id)
#     service.status = 'Done'
#     service.save()
#     messages.success(request, 'Service marked as Done!')
#     return redirect('manage_services')

# Delete Service
def delete_service(request, id):
    service = get_object_or_404(ServiceList, id=id)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('manage_services')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


