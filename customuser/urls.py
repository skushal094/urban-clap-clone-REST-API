from django.urls import path
from .views import add_comment , get_comment

urlpatterns = [
 path('add_comment/',add_comment),
 path('getcomment/', get_comment),

]