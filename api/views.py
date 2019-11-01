from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.models import Log, User
from api.serializers import LogsModelSerializer, UserModelSerializer


class LogsAPIView(APIView): 

    def get(self, request):
        log = Log.objects.all()
        serializer = LogsModelSerializer(log, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogsModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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

@permission_classes([AllowAny])
class UserAPIView(APIView):
    serializer_class = UserModelSerializer

    def get(self, request):
        user = User.objects.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            #Criação Token do usuário
            token = Token.objects.create(user=instance)
            
            response = serializer.data
            response['token'] = token.key 

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)