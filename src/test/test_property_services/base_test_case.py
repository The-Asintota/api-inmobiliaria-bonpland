from services.property.models import Home, Department, Local
from rest_framework.test import  APITestCase
from .factory.property import PropertyFactory

class BaseTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Load initial data for the TestCase.
        """
        if not (Home.objects.count() and Department.objects.count() and Local.objects.count()):
            PropertyFactory().create_test_data()