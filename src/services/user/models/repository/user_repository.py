from typing import Dict
from services.user.models import Users


class UserRepository:
    """
    UserRepository is a class that provides an abstraction of the database operations for the `Users` model.s
    """

    __model = Users.objects

    @classmethod
    def insert(cls, data: Dict[str, str]) -> None:
        """
        Inserts a new user into the database.
        """

        try:
            cls.__model.create_user(**data)
        except Exception:
            raise cls.UserRepositoryError('Failed to insert user data into the database.')


    class UserRepositoryError(Exception):
        """
        Custom exception for UserRepository errors.
        """

        def __init__(self, message: str) -> None:
            self.message = message
            super().__init__(self.message)
