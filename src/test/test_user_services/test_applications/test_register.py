from typing import Dict
from unittest import TestCase
from django.contrib.auth import get_user_model
from services.user.application.register import RegisterUser
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestRegister(TestCase):
    """
    Test case for the `RegisterUser application` service.

    This test case ensures that the user registration process works correctly. It uses the UserFactory to generate `fake user data` for testing. The tests are designed to verify that a user can be registered successfully and that the user data is stored correctly in the database.

    Attributes:
    - application_class: The class of the application service to be tested.
    - factory: The factory class used to generate fake user data.
    """

    application_class = RegisterUser
    factory = UserFactory

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = get_user_model().objects

    @parameterized.expand(
        input=[
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
            },)
        ],
    )
    def test_application_completed(self, data: Dict[str, str]) -> None:
        """
        This test verifies that a user can be registered successfully and that the user data is stored correctly in the database.

        Args:
        - data: A dictionary containing the user data to be used for registration.
        """

        # Verify that the user does not exist.
        user = self.model.filter(email=data['email']).first()
        self.assertIsNone(user)

        # Register the user.
        register = self.application_class(data)
        self.assertTrue(register.is_completed())
        self.assertEqual(register.errors, {})

        # Verify that the user exists.
        user = self.model.filter(email=data['email']).first()
        self.assertIsNotNone(user)

        # Verify that the user data is correct.
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
