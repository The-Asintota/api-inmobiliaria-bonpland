from typing import Dict, Any
from rest_framework.test import APITestCase
from services.property.infrastructure.serializers import(
    PropertySerializer, GetPropertySerializer
)
from test.test_property_services.factory import PropertyFactory
from parameterized import parameterized
from bson import ObjectId


class TestPropertySerializer(APITestCase):
    """
    This class is used to test the `PropertySerializer` class. It inherits from APITestCase which is a subclass of TestCase.
    """

    factory = PropertyFactory
    serializer_class = PropertySerializer

    @parameterized.expand(
        input=[
            (factory.get_data_home(),),
            (factory.get_data_department(),),
            (factory.get_data_local(),),
        ]
    )
    def test_serializer_is_valid(self, data: Dict[str, Any]) -> None:
        """
        This method tests the `is_valid` method of the `PropertySerializer` class. It verifies that the serializer correctly validates the data and that the data does not undergo any unexpected modifications.

        Args:
        - data (Dict[str, Any]) : The data to be validated by the serializer.
        """
        
        # Verify that the serializer validates the data correctly
        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, data)
        
        # Verify that the data did not suffer an unexpected modification
        for field, value in serializer.validated_data.items():
            self.assertEqual(value, data[field])


class TestGetPropertySerializer(APITestCase):
    """
    This class is used to test the `GetPropertySerializer` class. It inherits from APITestCase which is a subclass of TestCase.
    """

    factory = PropertyFactory
    serializer_class = GetPropertySerializer

    @parameterized.expand(
        input=[
            ({
                'pk': str(ObjectId())
            },),
            ({
                'pk': str(ObjectId())
            },),
            ({
                'pk': str(ObjectId())
            },),
        ]
    )
    def test_serializer_is_valid(self, data: Dict[str, str]) -> None:
        """
        This method tests the `is_valid` method of the `GetPropertySerializer` class. It verifies that the serializer correctly validates the data and that the data does not undergo any unexpected modifications.

        Args:
        - data (Dict[str, str]) : The data to be validated by the serializer.
        """
        
        # Verify that the serializer validates the data correctly
        serializer = self.serializer_class(data=data)
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
                'pk': '52155CS54DASA688SDA',
            },),
            ({
                'pk': 1,
            },)
        ]
    )
    def test_serializer_is_invalid(self, data: Dict[str, str]) -> None:
        """
        This method tests the `is_valid` method of the `GetPropertySerializer` class. It verifies that the serializer correctly identifies invalid data and returns appropriate errors.

        Args:
        - data (Dict[str, str]): The invalid data to be validated by the serializer.
        """
        
        # Verify that the serializer validates the data correctly
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        self.assertEqual(serializer.initial_data, data)
        self.assertEqual(serializer.validated_data, {})