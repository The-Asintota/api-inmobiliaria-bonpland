from typing import Dict, Any
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from services.user.models.repository import JwtRepository
from .base_aplication import AbstractUseCase
from backend.settings.base import SIMPLE_JWT
from jwt import decode


class UserAuthentication(AbstractUseCase):
    """
    UserAuthentication is a class that handles the authentication of users in the real estate management system.
    It extends the AbstractUseCase class and uses JSON Web Tokens (JWT) for authentication.
    """

    _authentication_class = TokenObtainPairSerializer
    _repository = JwtRepository

    def __init__(self, request_data: Request) -> None:
        super().__init__(data=request_data)
        self._tokens = {}

    @property
    def tokens(self) -> Dict[str, str]:
        return self._tokens

    @tokens.setter
    def tokens(self, value: Dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError('The errors property must be a dictionary')
        self._tokens = value

    @classmethod
    def _decoded_token(cls, token: str) -> Dict[str, Any]:
        """
        Decodes the given JWT.
        """

        return decode(
            jwt=token,
            key=SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[SIMPLE_JWT['ALGORITHM']],
        )

    @classmethod
    def authenticate_user(cls, data: Dict[str, str]) -> bool:
        """
        Authenticates the user with the given data.
        """

        authentication = cls._authentication_class(data=data)
        if authentication.is_valid():
            cls.tokens = authentication.validated_data
            access_token_payload = cls._decoded_token(cls.tokens['access'])
            try:
                cls._repository.create(
                    payload=access_token_payload,
                    token=cls.tokens['access'],
                    model='outstanding',
                    user=authentication.user,
                )
            except cls._repository.UserRepositoryError as e:
                cls._repository.delete(cls.tokens['refresh'])
                cls.errors['code_error'] = 'database_error'
                cls.errors['details'] = e.message
                raise

    def is_completed(self) -> bool:
        try:
            self.authenticate_user(self.data)
            return True
        except self._repository.UserRepositoryError:
            return False
