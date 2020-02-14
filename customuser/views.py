from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import  CommentSerializer, UserProfileSerializer
from .models import Comment, UserProfile
from django.contrib.auth.hashers import check_password,make_password


""""this function is used to add new comment """

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


@api_view(['PUT'])
@csrf_exempt
@permission_classes([AllowAny,])
def change_password(request):
    data = request.data
    print("request data==>",request.data)
    # service_req = ServiceRequest.objects.filter(pk=request.data['id']).update(status = request.data['status'])
    user_profile = UserProfile.objects.get(pk=data['id'])
    if check_password(request.data['password1'], user_profile.password):
        serializer = UserProfileSerializer(user_profile,data={'password':make_password(request.data['password'])})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors, status=400)
    else:
        print(check_password(request.data['password1'], user_profile.password))
        return Response('Error 400', status=400)
@api_view(['PUT'])
@csrf_exempt
@permission_classes([AllowAny,])
def delete_user(request):
    data = request.data
    print()
    print("request data==>",request.data)
    # service_req = ServiceRequest.objects.filter(pk=request.data['id']).update(status = request.data['status'])
    user_profile = UserProfile.objects.get(pk=data['id'])
    print("userpassword=========>",user_profile.password)
    print(check_password(request.data['password'], user_profile.password))
    if check_password(request.data['password'], user_profile.password):
        user_profile.delete()
        return Response('Succses',status=200)
    else:

        return Response('Error 400', status=400)