from typing import Dict
from unittest import TestCase
from services.user.infrastructure.serializers import AuthUserSerializer
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestCreateUserSerializer(TestCase):
    """
    Test case for the AuthUserSerializer class.

    This class contains unit tests that validate the behavior of the AuthUserSerializer class. The AuthUserSerializer is responsible for serializing and deserializing the user authentication data.
    """

    _serializer_class = AuthUserSerializer
    factory = UserFactory

    @parameterized.expand(
        input=[
            ({
                'email': factory.fake.email(),
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                )
            },)
        ]
    )
    def test_serializer_is_valid(self, data: Dict[str, str]) -> None:
        """This test case validates that the AuthUserSerializer correctly validates and serializes the user authentication data when the input data is valid.

        Args:
        - data (Dict[str, str]): The user authentication data to be validated and serialized.
        """

        # Verify that the serializer is valid.
        serializer = self._serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, data)

        # Verify that the validated data matches the input.
        for field, value in serializer.validated_data.items():
            self.assertEqual(value, data[field])

    @parameterized.expand(
        input=[
            ({
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
            },),
            ({
                'email': factory.fake.email(),
            },),
            ({
                'email': factory.fake.email(),
                'password': factory.fake.password(
                    length=6,
                    special_chars=False
                ),
            },),
            ({
                'email': 'email_invalid.com',
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                )
            },),
        ]
    )
    def test_serializer_is_invalid(self, data: Dict[str, str]) -> None:
        """
        This test case validates that the AuthUserSerializer correctly identifies invalid  user authentication data and provides appropriate error messages.

        Args:
        - data (Dict[str, str]): The user authentication data to be validated and serialized.
        """

        # Verify that the serializer is not valid.
        serializer = self._serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertNotEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, data)
