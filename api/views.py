from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from api.models import Log, User
from api.serializers import LogsModelSerializer, UserModelSerializer

class LogsDetail(APIView): 
    def get_object(self, id):
        try:
            return Log.objects.get(id=id)
        except Log.DoesNotExist:
            raise Http404

    def get(self, request, id):
        log = get_object_or_404(Log, id=id)
        serializer = LogsModelSerializer(log)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        log = self.get_object(id)
        serializer = LogsModelSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        log = self.get_object(id)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class UserDetail(APIView): 
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        user = self.get_object(id)
        serializer = UserModelSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        user = self.get_object(id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)