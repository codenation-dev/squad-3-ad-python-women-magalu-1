from django import forms

from api.models import Logs

class LogsModelForm(forms.ModelForm):
    class Meta:
        model = Logs
        fields = ['level', 'description', 'code_error', 'environment', 'status']  #, 'date_create']