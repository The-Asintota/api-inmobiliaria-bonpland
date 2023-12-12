from typing import Dict
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.forms.models import model_to_dict
from services.property.models.constants import PropertyType
from test.test_property_services.factory import PropertyFactory


class TestGetPropertyView(APITestCase):

    __factory = PropertyFactory()

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Load initial data for the TestCase.
        """

        cls.home_instance = cls.__factory.create_home_instance(
            data=cls.__factory.get_data_home()
        )
        cls.department_instance = cls.__factory.create_department_instance(
            data=cls.__factory.get_data_department()
        )
        cls.local_instance = cls.__factory.create_local_instance(
            data=cls.__factory.get_data_local()
        )

    def test_handle_valid_request(self) -> None:
        data = [
            {
                'pk': self.home_instance.id,
                'type_property': PropertyType.HOME.value
            },
            {
                'pk': self.department_instance.id,
                'type_property': PropertyType.DEPARTMENT.value
            },
            {
                'pk': self.local_instance.id,
                'type_property': PropertyType.LOCAL.value
            }
        ]
        for kwargs in data:
            # Check response
            response = self.client.get(reverse('get_property', kwargs=kwargs))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Compare response data with database data
            property_data: Dict = response.data
            property_features: Dict = property_data.pop('features')
            property_data.update(property_features)
            model = self.__factory.get_model_instance(kwargs['type_property'])
            property_instance = model_to_dict(model.objects.get(id = kwargs['pk']))
            self.assertEqual(property_data, property_instance)
    
    def test_handle_invalid_request(self) -> None:
        data = [
            {
                'pk': '325003-9e04812-bc726449651105',
                'type_property': PropertyType.HOME.value
            },
            {
                'pk': '325003-9e04812-bc726449651105',
                'type_property': PropertyType.DEPARTMENT.value
            },
            {
                'pk': '325003-9e04812-bc726449651105',
                'type_property': PropertyType.LOCAL.value
            },
        ]
        for kwargs in data:
            # Check response
            response = self.client.get(reverse('get_property', kwargs=kwargs))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)