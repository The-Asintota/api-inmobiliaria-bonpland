from typing import Dict
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from services.user.application import UserAuthentication
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestAuthentication(TestCase):
    """
    TestAuthentication is a test case for the `UserAuthentication` application.

    This class tests the functionality of the UserAuthentication application in the context of a real estate management system.
    It verifies the user registration process, token generation and storage, and the association of tokens with the user.

    Attributes:
    - factory (UserFactory) : A factory for creating user instances for testing.
    - model (User) : The user model used in the tests.
    """

    _application_class = UserAuthentication
    factory = UserFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = get_user_model().objects

    @parameterized.expand(
        input=[
            ({
                'email': factory.fake.email(),
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                ),
            },)
        ],
    )
    def test_application_completed(self, data: Dict[str, str]) -> None:
        """
        This method tests the user registration process, token generation and storage, and the association of tokens with the user.
        It verifies that the application is completed without errors and that the tokens are stored in the database and associated with the user.

        Args:
        - data (Dict[str, str]) : The user data to be used in the test.
        """

        user = self.model.create_user(**data)

        # Test authentication user.
        register = self._application_class(data)
        self.assertTrue(register.is_completed())
        self.assertEqual(register.errors, {})
        self.assertIsNotNone(register.tokens.get('access', None))
        self.assertIsNotNone(register.tokens.get('refresh', None))

        # Verify that the tokens are stored in the database.
        access_token = OutstandingToken.objects.filter(
            token=register.tokens['access']
        ).first()
        refresh_token = OutstandingToken.objects.filter(
            token=register.tokens['refresh']
        ).first()
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

        # Verify that the tokens are associated with the user.
        self.assertEqual(access_token.user, user)
        self.assertEqual(refresh_token.user, user)
