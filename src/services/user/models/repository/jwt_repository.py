from typing import Dict
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken, BlacklistedToken
)
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import pytz


class JwtRepository:
    """
    JwtRepository is a class that manages the storage of previously created JWT tokens.
    Interacts with the OutstandingToken and BlacklistedToken models from the Django Rest Framework's simplejwt package.
    """

    _out_stanfing_token = OutstandingToken.objects
    _blacklisted_token = BlacklistedToken.objects

    @classmethod
    def create(cls, payload: Dict[str, str], token: str, model: str, user: AbstractUser) -> None:
        """
        Creates a new outstanding token record in the database.
        """

        if model == 'outstanding':
            try:
                cls._out_stanfing_token.create(
                    jti=payload['jti'],
                    token=token,
                    user=user,
                    created_at=datetime.now(pytz.UTC),
                    expires_at=datetime_from_epoch(payload['exp']),
                )
            except Exception:
                raise cls.UserRepositoryError(
                    'Failed to insert user data into the database.'
                )

    @classmethod
    def delete(cls, token: str) -> None:
        """
        Deletes an outstanding token record from the database.
        """

        cls._out_stanfing_token.get(token=token).delete()


    class UserRepositoryError(Exception):
        """
        Custom exception for UserRepository errors.
        """

        def __init__(self, message: str) -> None:
            self.message = message
            super().__init__(self.message)
