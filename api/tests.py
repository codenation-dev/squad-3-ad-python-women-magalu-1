import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.test import TestCase
from django.test.client import Client
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

    '''def test_token(self):
        params = {"username": "squadum@gmail.com", "password": "xxxxxxxxxxxxxxxxxxxxxxx"}
        response = self.client.post('/token_auth/', params, content_type='application/json')

        assert isinstance(response.data, dict)
        self.assertEqual(response.status_code, 200)'''