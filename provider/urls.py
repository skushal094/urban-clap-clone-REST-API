from django.urls import path
from .views import add_service,delete_service, change_status

urlpatterns = [
 path('addservice/',add_service),
 path('deleteservice/', delete_service),
 path('changestatus/', change_status),

]