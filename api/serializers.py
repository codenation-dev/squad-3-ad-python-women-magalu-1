from rest_framework import serializers
from api.models import Log, User

class LogsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ["level", "description", "code_error", "environment", "status", "details"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
        

# Criar novo usuário no sistema
class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs={'password': {'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        
        # senha armazenada em hash
        user.set_password(password)
        user.save()
        return user