from django.urls import path
from .views import get_services

urlpatterns = [
 path('getservices',get_services),

]