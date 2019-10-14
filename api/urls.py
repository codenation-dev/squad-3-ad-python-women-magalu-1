from django.urls import include, path, re_path

from rest_framework import routers

from api import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]