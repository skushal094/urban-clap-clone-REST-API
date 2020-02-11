from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=['user','s_request','timestamp','comment',]