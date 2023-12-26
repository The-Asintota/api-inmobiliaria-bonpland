from django.urls import path
from .views import RegisterUserAPIView, UserAuthAPIView


urlpatterns = [
    path('user/', view=RegisterUserAPIView.as_view(), name='create_user'),
    path('user/auth/', view=UserAuthAPIView.as_view(), name='auth_user'),
]
