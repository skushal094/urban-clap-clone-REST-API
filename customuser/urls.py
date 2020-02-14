from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUpUser.as_view()),
    path('logout/', views.LogoutUser.as_view()),
    path('add_comment/', views.add_comment),
   path('getcomment/', views.get_comment),
   path('changepassword/', views.change_password),
   path('deleteuser/', views.delete_user),
]
