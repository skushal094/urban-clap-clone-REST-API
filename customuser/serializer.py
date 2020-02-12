from rest_framework import serializers
from .models import Comment, UserProfile

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=['user','s_request','timestamp','comment',]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["password",]
