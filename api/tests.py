import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.test import TestCase
from django.test.client import Client

import base64

from rest_framework.authtoken.models import Token

from api.models import User, Log

#python manage.py test

class TesteCentralErros(TestCase):

    def setUp(self):
        user = User.objects.create(username="SquadUm", first_name="Squad", last_name="Um", email="squadum@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx")
        Log.objects.create(level="critical", description="django.core.exceptions.ValidationError", code_error=1, environment="desenvolvimento", details="File '/home/alireza/test/lib/python3.4/site-packages/django/db/models/fields/__init__.py', line 1252", user=user)
        self.client = Client()


    def test_model_user(self):
        user = User.objects.get(username="SquadUm")
        self.assertEqual(user.email, "squadum@gmail.com")

    def test_model_log(self):
        log = Log.objects.get(code_error=1)
        self.assertEqual(log.level, "critical")

    def test_create_user(self):
        params = {
            "username": "squadtres",
            "first_name": "squad",
            "last_name": "tres",
            "email": "squadtres@gmail.com",
            "password": "xxxxxxxxxxxxxxxxxxxxxxx"
        }

        response = self.client.post('/api/user/', params, content_type='application/json')

        assert isinstance(response.data, dict)        
        self.assertEqual(response.status_code, 201)

    def test_create_token(self):
        params = {
            "username": "squadtres",
            "first_name": "squad",
            "last_name": "tres",
            "email": "squadtres@gmail.com",
            "password": "xxxxxxxxxxxxxxxxxxxxxxx"
        }

        self.client.post('/api/user/', params, content_type='application/json')

        token = Token.objects.all()

        self.assertEqual(
            token.count(),
            1
        )

    
    def test_create_logs(self):
        params = {
            "username": "squadtres",
            "first_name": "squad",
            "last_name": "tres",
            "email": "squadtres@gmail.com",
            "password": "xxxxxxxxxxxxxxxxxxxxxxx"
        }
        
        response = self.client.post('/api/user/', params, content_type='application/json')
        
        user = User.objects.get(email="squadtres@gmail.com")
        token = Token.objects.get(user_id=user)
        token_id = token.key

        params = {
            "level": "critical", 
            "description": "django.core.exceptions.ValidationError", 
            "code_error": 1, 
            "environment": "desenvolvimento", 
            "status": "ativo",
            "details": "File '/home/alireza/test/lib/python3.4/site-packages/django/db/models/fields/__init__.py', line 1252"
        }

        authorization_token = "Token "+token_id

        headers = {
            "HTTP_AUTHORIZATION": authorization_token
        }

        response = self.client.post('/api/logs/', params, content_type='application/json', **headers)

        assert isinstance(response.data, dict)        
        self.assertEqual(response.status_code, 201) 