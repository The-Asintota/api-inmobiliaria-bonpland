from django.urls import path
from .views import RegisterUserAPIView


urlpatterns = [
    path('user/', view=RegisterUserAPIView.as_view(), name='create_user'),
]
