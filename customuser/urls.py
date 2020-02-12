from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUpUser.as_view()),
    path('logout/', views.LogoutUser.as_view())
]
