from typing import Dict
from unittest import TestCase
from services.user.infrastructure.serializers import CreateUserSerializer
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestCreateUserSerializer(TestCase):
    """
    Unit Test Case for the `CreateUserSerializer class` in the User Service.

    This class contains unit tests that validate the behavior of the CreateUserSerializer. The CreateUserSerializer is responsible for validating and deserializing input data for user creation in the real estate management system's API.

    Attributes:
    - serializer_class: The class of the serializer that is being tested.
    - factory: The factory class used to generate fake data for testing.
    """

    serializer_class = CreateUserSerializer
    factory = UserFactory

    @parameterized.expand(
        input=[
            ({
                'email': factory.fake.email(),
                'password': 'Aaa123456789',
                'confirm_password': 'Aaa123456789'
            },)
        ],
    )
    def test_serializer_is_valid(self, data: Dict[str, str]) -> None:
        """
        This test verifies that the CreateUserSerializer correctly validates and deserializes the input data when the data is valid. It checks that the serializer reports no errors and that the validated data matches the input data.

        Args:
        - data: A dictionary containing valid user data.
        """

        # Verify that the serializer is valid.
        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, data)

        # Verify that the validated data matches the input.
        for field, value in serializer.validated_data.items():
            self.assertEqual(value, data[field])

    @parameterized.expand(
        input=[
            ({
                'email': factory.fake.email(),
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                )
            },),
            ({
                'email': factory.fake.email(),
                'confirm_password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
            },),
            ({
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
                'confirm_password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
            },),
            ({
                'email': factory.fake.email(),
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
                'confirm_password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
            },),
            ({
                'email': ['my_correo@correo.com'],
                'password': ['my_password'],
                'confirm_password': ['my_password'],
            },)
        ],
    )
    def test_serializer_is_not_valid(self, data: Dict[str, str]) -> None:
        """
        This test verifies that the CreateUserSerializer correctly identifies invalid input data. It checks that the serializer reports errors and that no data is validated when the input data is invalid.

        Args:
        - data: A dictionary containing invalid user data.
        """

        # Verify that the serializer is invalid.
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertNotEqual(serializer.errors, {})
        self.assertEqual(serializer.validated_data, {})
