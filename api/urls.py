from django.urls import include, path, re_path

from rest_framework import routers

from api import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', views.LogsAPIView.as_view()),
    path('logs/<int:id>', views.LogsDetail.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:id>', views.UserDetail.as_view())
]