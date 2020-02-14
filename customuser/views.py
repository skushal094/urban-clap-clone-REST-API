from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import Comment, UserProfile
from django.contrib.auth.hashers import check_password,make_password
from .serializers import SignUpSerializer
from .serializer import CommentSerializer, UserProfileSerializer


class SignUpUser(APIView):
    """This function perform signing up of user"""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Handles POST method"""
        user = SignUpSerializer(data=request.data)
        if user.is_valid():
            user = user.create(user.validated_data)
            data = {'message': 'User created successfully', 'email': user.email, 'username': user.name}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):
    """Used to log user out"""
    def post(self, request):
        """Handles POst method"""
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'error logging you out.'}, status=status.HTTP_401_UNAUTHORIZED)


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
        return Response('Error 400', status=400)
      
      
@api_view(['PUT'])
@csrf_exempt
@permission_classes([AllowAny,])
def delete_user(request):
    data = request.data
    # service_req = ServiceRequest.objects.filter(pk=request.data['id']).update(status = request.data['status'])
    user_profile = UserProfile.objects.get(pk=data['id'])
    if check_password(request.data['password'], user_profile.password):
        user_profile.delete()
        return Response('Succses',status=200)
    else:

        return Response('Error 400', status=400)
