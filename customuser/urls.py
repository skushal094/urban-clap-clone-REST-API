from django.urls import path
from .views import add_comment , get_comment,change_password,delete_user

urlpatterns = [
 path('add_comment/',add_comment),
 path('getcomment/', get_comment),
 path('changepassword/', change_password),
 path('deleteuser/', delete_user),

]