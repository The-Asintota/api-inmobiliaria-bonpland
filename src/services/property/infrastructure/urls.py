from django.urls import path
from .views import SearchPropertyAPIView, GetPropertyAPIView


urlpatterns = [
    path('search/', SearchPropertyAPIView.as_view(), name='search_property'),
    path('property/<str:type_property>/<str:pk>/', GetPropertyAPIView.as_view(), name='get_property'),
]