from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SignUpSerializer


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
