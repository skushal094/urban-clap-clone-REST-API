from django.urls import path
from . import views

urlpatterns = [
    path('create-request/', views.ServiceRequestCreate.as_view()),
    path('delete-request/<int:pk>/', views.delete_request),
    path('get-request/<int:pk>/', views.RetrieveRequest.as_view()),
    path('get-my-request/', views.RetrieveForCustomerRequest.as_view()),
    path('getservices',views.get_services),
]
