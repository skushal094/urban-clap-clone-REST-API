from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import ServiceSerializer,ServiceRequestSerializer
from .models import Service, ServiceRequest
# Create your views here.
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny,])
def add_service(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status=400)

@api_view(['DELETE'])
@csrf_exempt
@permission_classes([AllowAny,])
def delete_service(request):
    if request.method == 'DELETE':
        service = Service.objects.filter(pk=request.data['id']).all()
        serializer = ServiceSerializer(service).instance.delete()
        print('serializer========>',serializer)

        return Response({"status_code":200,"status":"success","message":"Service Deleted","data":[]},status=200)
    else:
        return Response(staus=400)

@api_view(['PUT'])
@csrf_exempt
@permission_classes([AllowAny,])
def change_status(request):
    data = request.data
    print("request data==>",request.data)
    # service_req = ServiceRequest.objects.filter(pk=request.data['id']).update(status = request.data['status'])
    service_req = ServiceRequest.objects.get(pk=data['id'])
    print("service===========================>",service_req.id)
    serializer = ServiceRequestSerializer(service_req,data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=200)
    else:
        return Response(serializer.errors, status=400)
