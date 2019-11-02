import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.test import TestCase
from django.test.client import Client

from rest_framework.authtoken.models import Token

from api.models import User, Log



class TesteCentralErros(TestCase):

    def setUp(self):
        user = User.objects.create(username="SquadUm", first_name="Squad", last_name="Um", email="squadum@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx")
        Log.objects.create(level="CRITICAL", description="django.core.exceptions.ValidationError", code_error=1, environment="desenvolvimento", user=user)
        self.client = Client()


    def test_model_user(self):
        user = User.objects.get(username="SquadUm")
        self.assertEqual(user.email, "squadum@gmail.com")

    def test_model_log(self):
        log = Log.objects.get(code_error=1)
        self.assertEqual(log.level, "CRITICAL")

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

