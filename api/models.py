from django.db import models
from django.core.validators import MinLengthValidator

class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8)])
    status = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Logs(models.Model):
    LEVELS_CHOICES = (
        ('critical', 'CRITICAL'),
        ('debug', 'DEBUG'),
        ('error', 'ERROR'),
        ('warning', 'WARNING'),
        ('info', 'INFO')
    )

    STATUS_CHOICES = (
        ('ativo', 'ATIVO'),
        ('inativo', 'INATIVO'),
        ('arquivado', 'ARQUIVADO')
    )
    ENVIRONMENTS_CHOICES = (
        ('desenvolvimento', 'DEV'),
        ('homologacao', 'HOMOLOGAÇÃO'),
        ('producao', 'PRODUÇÃO')
    )

    level = models.CharField(max_length=20, choices=LEVELS_CHOICES)
    description = models.TextField()
    code_error = models.IntegerField()
    environment = models.CharField(max_length=20, choices=ENVIRONMENTS_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs'
