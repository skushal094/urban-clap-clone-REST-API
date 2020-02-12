from rest_framework import serializers
from .models import UserProfile


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'name', 'type']

    def create(self, validated_data):
        user = UserProfile(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
        )
        user.set_password(validated_data.get('password'))
        user.type = validated_data.get('type') if validated_data.get('type', None) else 'Customer'
        user.save()
        return user
