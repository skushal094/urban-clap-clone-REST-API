from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import  CommentSerializer
from .models import Comment

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny,])
def add_comment(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,400)
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny,])
def get_comment(request):
    if request.method == 'GET':
        a=request.data['requestid']
        comments=Comment.objects.filter(s_request_id=a)
        serializer=CommentSerializer(comments,many=True)
        return Response( serializer.data,status=201 )
