from rest_framework import serializers

from api.models import Logs

class LogsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = ["level", "description", "code_error", "environment", "status"]  #, "date_create"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
        
'''
{
    "level": "error", 
    "description": "Erro ao cadastrar produto.", 
    "code_error": 400, 
    "environment": "producao", 
    "status": "ativo"
}
'''