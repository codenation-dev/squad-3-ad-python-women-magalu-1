from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MinLengthValidator


class MyUserManager(BaseUserManager):
    """
        Classe para sobreescrever a criação de usuários do django.
    """
    def create_user(self, email, name, password):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email,
            password=password,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8)])
    status = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    class Meta:
        db_table = 'users'


class Log(models.Model):
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
    user = models.ForeignKey('User', related_name='logs', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    date_create = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=200)

    class Meta:
        db_table = 'logs'
