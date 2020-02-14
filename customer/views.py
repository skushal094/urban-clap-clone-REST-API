from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import ServiceRequestSerializer, ServiceRequestDetailSerializer
from .serializer import ServiceSerializer
from rest_framework.response import Response
from rest_framework import status
from customuser.models import ServiceRequest, Service
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
class ServiceRequestCreate(APIView):
    """Handles creating service request"""
    def post(self, request):
        """Handles POST request"""
        if request.user.type != 'Customer':
            return Response(
                {'message': 'You are not allowed to create requests.'},
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            )
        data = ServiceRequestSerializer(data=request.data)
        if data.is_valid():
            req = data.create(data.validated_data)
            req.customer = request.user
            req.status_t = 'Pending'
            req.save()
            return Response({'message': 'service request created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_request(request, pk):
    """deletes service requests"""
    try:
        sr = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({
            'status_code': 404,
            'status': 'not found',
            'message': 'Service request doesn\'t exist',
        }, status=status.HTTP_404_NOT_FOUND)
    if sr.customer != request.user:
        return Response({
            'status_code': 401,
            'status': 'unauthorized',
            'message': "You don't have permission to delete this."
        }, status=status.HTTP_401_UNAUTHORIZED)
    if sr.status in ['Rejected', 'Completed']:
        sr.delete()
        return Response({
            'status_code': 204,
            'status': 'no content',
            'message': 'Service request deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({
            'status_code': 403,
            'status': 'forbidden',
            'message': 'This service request can\'t be deleted.'
        }, status=status.HTTP_403_FORBIDDEN)


class RetrieveRequest(APIView):
    """Returns particular request"""
    def get(self, request, pk):
        """Handles GET requests"""
        try:
            sr = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({
                'status_code': 404,
                'status': 'not found',
                'message': 'Service request doesn\'t exist',
            }, status=status.HTTP_404_NOT_FOUND)
        if sr.customer == request.user or sr.service.provider == request.user:
            serializer = ServiceRequestDetailSerializer(sr)
            return Response({
                'status_code': 200,
                'status': 'success',
                'message': "Service request with id: {}".format(pk),
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status_code': 401,
                'status': 'unauthorized',
                'message': "You don't have permission to delete this."
            }, status=status.HTTP_401_UNAUTHORIZED)


class RetrieveForCustomerRequest(APIView):
    """Returns particular request"""
    def get(self, request):
        """Handles GET requests"""
        if request.user.type == 'Service provider':
            return Response({
                'status_code': 401,
                'status': 'unauthorized',
                'message': "Providers can't have service requests"
            }, status=status.HTTP_401_UNAUTHORIZED)
        sr = ServiceRequest.objects.filter(customer=request.user)
        if len(sr) == 0:
            return Response({
                'status_code': 404,
                'status': 'not found',
                'message': 'No service requests exists',
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ServiceRequestDetailSerializer(sr, many=True)
            return Response({
                'status_code': 200,
                'status': 'success',
                'message': "Service request for user: {}".format(request.user.name),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

@csrf_exempt
@permission_classes([AllowAny,])
@api_view(['GET',])
def get_services(request):
    service = Service.objects.all()
    serializer = ServiceSerializer(service,many=True)
    return Response(serializer.data,status=200)
