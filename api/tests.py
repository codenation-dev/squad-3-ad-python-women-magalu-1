import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.test import TestCase
from api.models import Users, Logs


class TesteCentralErros(TestCase):

    def setUp(self):
        Users.objects.create(name="SquadUm", email="squadum@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx")
        Logs.objects.create(level="CRITICAL", description="django.core.exceptions.ValidationError", code_error=1, environment="desenvolvimento")

    def test_1(self):
        user = Users.objects.get(name="SquadUm")
        self.assertEqual(user.email, "squadum@gmail.com")

    def test_2(self):
        log = Logs.objects.get(code_error=1)
        self.assertEqual(log.level, "CRITICAL")