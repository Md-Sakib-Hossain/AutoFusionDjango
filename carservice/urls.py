from django.urls import path
from carservice import views
urlpatterns = [
    path('car_service',views.car_service,name="car_service"),
    path('appointment',views.appointment,name="appointment"),
    path('servicelist',views.servicelist,name="servicelist"),
    path('insert',views.insertData,name="insertData"),
    path('insertservice',views.insertservice,name="insertservice"),
    path('adminservice',views.adminservice,name="adminservice"),
    path('manageservice',views.manageservice,name="manageservice"),
    
    path('adminservice/', views.manage_services, name='manage_services'),
    path('adminservice/done/', views.mark_service_done, name='mark_service_done'),
    path('adminservice/delete/<int:id>/', views.delete_service, name='delete_service'),
    path('adminservice/arrived/<int:service_id>/', views.mark_service_arrived, name='mark_service_arrived'),
    
]
