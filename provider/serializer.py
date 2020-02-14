from .models import Service, ServiceRequest
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields=['provider','service','cost','description',]

class ServiceRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceRequest
        fields = "__all__"
        read_only_fields = ('id','customer',"service","timestamp")