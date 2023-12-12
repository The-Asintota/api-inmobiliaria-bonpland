from typing import Dict, Any
from rest_framework.test import APITestCase
from parameterized import parameterized
from services.property.infrastructure.serializers import PropertySerializer, GetPropertySerializer
from services.property.models.constants import PropertyType
from test.test_property_services.factory import PropertyFactory


class TestPropertySerializer(APITestCase):
    """
    This class is used to test the PropertySerializer class. It inherits from APITestCase which is a subclass of TestCase.

    Attributes:
    - __factory (PropertyFactory): The factory used to generate test data.
    - __serializer_class (PropertySerializer): The class of the serializer that is being tested.
    """

    __factory = PropertyFactory()
    __serializer_class = PropertySerializer

    @parameterized.expand(
        input=[
            (__factory.get_data_home(),),
            (__factory.get_data_department(),),
            (__factory.get_data_local(),),
        ]
    )
    def test_serializer_is_valid(self, property_data: Dict[str, Any]) -> None:
        # Verify that the serializer validates the data correctly
        property_data['id'] = '325b003c-9e02-4812-bc72-a64496511056'
        property_data['date_joined'] = '2023-10-11 00:38:14.210167+00:00'
        serializer = self.__serializer_class(data=property_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, property_data)
        
        # Verify that the data did not suffer an unexpected modification
        property_description = serializer.to_representation(property_data)
        property_features: Dict = property_description.pop('features')
        for field, value in property_description.items():
            self.assertEqual(value, property_data[field])
        for field, value in property_features.items():
            self.assertEqual(value, property_data[field])


class TestGetPropertySerializer(APITestCase):
    """
    This class is used to test the GetPropertySerializer class. It inherits from APITestCase which is a subclass of TestCase.

    Attributes:
    - __factory (PropertyFactory): The factory used to generate test data.
    - __serializer_class (GetPropertySerializer): The class of the serializer that is being tested.
    """

    __factory = PropertyFactory()
    __serializer_class = GetPropertySerializer

    @parameterized.expand(
        input=[
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': PropertyType.HOME.value,
            },),
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': PropertyType.DEPARTMENT.value,
            },),
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': PropertyType.LOCAL.value,
            },),
        ]
    )
    def test_serializer_is_valid(self, data: Dict[str, str]) -> None:
        # Verify that the serializer validates the data correctly
        serializer = self.__serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, data)
        
        # Verify that the data did not suffer an unexpected modification
        for field, value in serializer.validated_data.items():
            self.assertEqual(str(value), data[field])

    @parameterized.expand(
        input=[
            ({},),
            ({
                'type_property': PropertyType.DEPARTMENT.value,
            },),
            ({
                'pk': __factory.fake.uuid4(),
            },),
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': 'home',
            },),
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': 'casa',
            },),
            ({
                'pk': __factory.fake.uuid4(),
                'type_property': 10,
            },),
            ({
                'pk': '325003-9e04812-bc726449651105',
                'type_property': 'department',
            },),
        ]
    )
    def test_serializer_is_invalid(self, data: Dict[str, str]) -> None:
        # Verify that the serializer validates the data correctly
        serializer = self.__serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        self.assertEqual(serializer.initial_data, data)
        self.assertEqual(serializer.validated_data, {})
