from rest_framework import serializers
from customuser.models import ServiceRequest


class ServiceRequestSerializer(serializers.ModelSerializer):
    """serializes ServiceRequest model"""
    class Meta:
        model = ServiceRequest
        fields = ['service']

    def create(self, validated_data):
        req = ServiceRequest(
            service=validated_data.get('service')
        )
        return req


class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    """serializes a particular service request"""
    class Meta:
        model = ServiceRequest
        fields = ['customer', 'service', 'timestamp', 'status']
