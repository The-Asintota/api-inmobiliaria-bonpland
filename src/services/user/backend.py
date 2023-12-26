from typing import Optional
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser


class EmailBackend(ModelBackend):
    """
    A `custom authentication backend` that authenticates users based on their email and password.

    Attributes:
    - model: The user model used for authentication.
    """

    model = get_user_model().objects

    def authenticate(self, request: Request, email: str, password: str) -> Optional[AbstractUser]:
        """
        This method is used to authenticate a user. It checks if a user with the provided email exists, and if so, it checks if the provided password is correct.

        Args:
        - request (Request): The Django Rest request.
        - email (str): The email of the user to authenticate.
        - password (str): The password of the user to authenticate.
        """

        user = self.model.filter(email=email).first()
        if user:
            return user if user.check_password(password) else None
        return None
