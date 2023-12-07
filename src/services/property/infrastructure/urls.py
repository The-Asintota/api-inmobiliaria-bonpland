from django.urls import path
from .views import SearchPropertyAPIView


urlpatterns = [
    path('search/', SearchPropertyAPIView.as_view(), name='search_property'),
]