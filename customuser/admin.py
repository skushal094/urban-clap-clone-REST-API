from django.contrib import admin
from .models import UserProfile, Service, ServiceRequest, Comment


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(ServiceRequest)
admin.site.register(Comment)
