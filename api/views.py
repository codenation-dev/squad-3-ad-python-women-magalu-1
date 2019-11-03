from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from operator import itemgetter

from rest_framework import status, viewsets, generics, filters
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Log, User
from api.serializers import LogsModelSerializer, UserModelSerializer

class LogsDetail(APIView): 
    def get_object(self, id, user):
        try:
            return Log.objects.get(id=id, user=user)
        except Log.DoesNotExist:
            raise Http404

    def get(self, request, id):
        log = get_object_or_404(Log, id=id, user=request.user)
        serializer = LogsModelSerializer(log)
        count = Log.objects.filter(user=request.user, code_error=log.code_error).count()
        response = serializer.data
        response.update({'count_erros': count})
        return Response(response)
    
    def put(self, request, id, format=None):
        log = self.get_object(id=id, user=self.request.user)
        serializer = LogsModelSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        log = self.get_object(id=id, user=self.request.user)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogsAPIView(APIView): 
    def get(self, request):
        codes_erros = Log.objects.filter(user=request.user).values('code_error').annotate(Count('code_error'))
        query_params = request.query_params.dict()

        order = query_params.get('order', None)
        reverse = bool(int(query_params.get('reverse', 0)))

        if 'reverse' in query_params.keys():
            query_params.pop('reverse')

        if 'order' in query_params.keys():
            query_params.pop('order')

        response = []
        for code in codes_erros:
            query_params.update({'user': request.user,'code_error': code.get('code_error')})
            try:
                log = Log.objects.filter(**query_params).order_by('date_create').values().first()
            except:
                msg = f'Campos para pesquisa: code_error, date_create, description, details, environment, id, level, status'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

            if log:
                log.update({'count_erros': code.get('code_error__count')})
                response.append(log)

        if order:
            try:
                response = sorted(response, key=itemgetter(order), reverse=reverse) 
            except:
                msg = f'Campos para ordenar: code_error, date_create, description, details, environment, id, level, status, count_erros'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = LogsModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@permission_classes([AllowAny])
class UserAPIView(APIView):
    serializer_class = UserModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            #Criação Token do usuário
            token = Token.objects.create(user=instance)
            
            response = serializer.data
            response.update({'token': token.key}) 

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView): 
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        if id == request.user.id:
            user = get_object_or_404(User, id=id)
        else:
            return Response({'detail': 'ID do usuário inválido'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserModelSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        if id == request.user.id:
            user = self.get_object(id=id)
        else:
            return Response({'detail': 'ID do usuário inválido'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserModelSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        if id == request.user.id:
            user = self.get_object(id=id)
        else:
            return Response({'detail': 'ID do usuário inválido'}, status=status.HTTP_401_UNAUTHORIZED)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)