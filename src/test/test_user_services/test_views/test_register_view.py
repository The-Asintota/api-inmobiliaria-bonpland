from typing import Dict
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestRegisteUserView(APITestCase):
    """
    Test case for the user registration view.

    This class contains unit tests that validate the behavior of the user registration view, which is a subclass of Django's TestCase with additional features for testing Django REST framework views.
    """

    factory = UserFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = get_user_model().objects
        cls.url = reverse('create_user')

    @parameterized.expand(
        input=[
            ({
                'email': factory.fake.email(),
                'password': 'Aaa123456789',
                'confirm_password': 'Aaa123456789'
            },)
        ]
    )
    def test_handle_valid_request(self, data: Dict[str, str]) -> None:
        """
        This method tests the behavior of the registration view when it receives a valid request. It verifies that the user is created correctly and that the response status code is 201.

        Args:
        - data: A dictionary containing valid user data.
        """

        # Verify that the user exists.
        self.assertFalse(self.model.filter(email=data['email']).exists())

        # Verify that the view returns a status code of 201.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

        # Verify that the user data is correct.
        user = self.model.filter(email=data['email']).first()
        self.assertIsNone(user.dni)
        self.assertIsNone(user.full_name)
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertIsNone(user.phone_number)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

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
            },),
            ({
                'email': factory.fake.email(),
                'password': 'Aaa123456789',
            },),
            ({
                'email': factory.fake.email(),
                'confirm_password': 'Aaa123456789',
            },),
        ]
    )
    def test_handle_invalid_request(self, data: Dict[str, str]) -> None:
        """
        This method tests the behavior of the registration view when it receives an invalid request. It verifies that the user is not created and that the response status code is 400.

        Args:
        - data: A dictionary containing invalid user data.
        """

        # Verify that the user exists.
        self.assertFalse(self.model.filter(email=data['email']).exists())

        # Verify that the view returns a status code of 400.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

        # Verify that the user exists.
        self.assertFalse(self.model.filter(email=data['email']).exists())
