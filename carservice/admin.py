from django.contrib import admin
from .models import ServiceList

from .models import Service  

admin.site.register(Service)

admin.site.register(ServiceList)