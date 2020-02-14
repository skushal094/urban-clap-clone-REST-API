from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from .serializer import ServiceSerializer
from .models import Service

@csrf_exempt
@permission_classes([AllowAny,])
@api_view(['GET',])
def get_services(request):
    service = Service.objects.all()
    serializer = ServiceSerializer(service,many=True)
    return Response(serializer.data,status=200)
