from django.urls import path
from .views import SearchPropertyAPIView, GetPropertyAPIView


urlpatterns = [
    path('property/search/', SearchPropertyAPIView.as_view(), name='search_property'),
    path('property/<str:pk>/', GetPropertyAPIView.as_view(), name='get_property'),
]
