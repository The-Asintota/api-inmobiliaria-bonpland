from typing import Dict
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.contrib.auth import get_user_model
from django.urls import reverse
from test.test_user_services.factory import UserFactory
from parameterized import parameterized


class TestAuthUserView(APITestCase):
    """
    Test case for the authentication view of the real estate management system API.

    This test case uses the Django Rest Framework's APITestCase as a base, and tests
    the functionality of the authentication view, which is responsible for handling
    user authentication requests.

    Attributes:
    - factory: A UserFactory instance used to generate fake user data for testing.
    - model: The user model used by the authentication view.
    - url: The URL of the authentication view.
    """

    factory = UserFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = get_user_model().objects
        cls.url = reverse('auth_user')

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
    def test_handle_valid_request(self, data: Dict[str, str]) -> None:
        """
        This test case sends a valid authentication request to the authentication view,
        and checks that the response has a status code of 200, that the tokens are stored
        in the database, and that the user data is correct.

        Args:
        - data (Dict[str, str]) : A dictionary containing valid user data.
        """

        self.model.create_user(**data)

        # Verify that the view returns a status code of 200.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # Verify that the tokens are stored in the database.
        access_token = OutstandingToken.objects.filter(
            token=response.data['access']
        ).first()
        refresh_token = OutstandingToken.objects.filter(
            token=response.data['refresh']
        ).first()
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

        # Verify that the user data is correct.
        self.assertEqual(response.data['access'], access_token.token)
        self.assertEqual(response.data['refresh'], refresh_token.token)

    @parameterized.expand(
        input=[
            ({
                'email': 'email_invalid.com',
                'password': factory.fake.password(
                    length=6,
                    special_chars=False
                )
            },),
            ({
                'email': factory.fake.email()
            },),
            ({
                'password': factory.fake.password(
                    length=10,
                    special_chars=False
                )
            },),
        ]
    )
    def test_if_invalid_data(self, data: Dict[str, str]) -> None:
        """
        This test case sends an authentication request with invalid data to the
        authentication view, and checks that the response has a status code of 400.

        Args:
        - data (Dict[str, str]) : A dictionary containing invalid user data.
        """

        # Verify that the view returns a status code of 400.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

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
    def test_if_user_not_exists(self, data: Dict[str, str]) -> None:
        """
        This test case sends an authentication request for a non-existent user to the
        authentication view, and checks that the response has a status code of 401.

        Args:
        - data: A dictionary containing user data for a non-existent user.
        """

        # Verify that the view returns a status code of 401.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)
