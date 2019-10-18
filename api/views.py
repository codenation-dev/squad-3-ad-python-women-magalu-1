from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from api.models import Logs
from api.serializers import LogsModelSerializer

# Create your views here.

class LogsAPIView(APIView): 

    def get(self, request):
        log = Logs.objects.all()
        serializer = LogsModelSerializer(log, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogsModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['POST'])
def cadastrar_erro(request):
    serializer = LogsSerializer(request.data)

    if serializer.is_valid()():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    #serializer = LogsSerializer()
    return Response(status=status.HTTP_400_BAD_REQUEST) 
'''

