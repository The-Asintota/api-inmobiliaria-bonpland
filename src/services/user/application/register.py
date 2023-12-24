from typing import Dict
from services.user.models.repository import UserRepository


class RegisterUser:
    """
    Use case that creates a user in the system.

    Attributes:
    - data (Dict[str, str]) : a dictionary containing user data for registration.
    - errors (Dict[str, str]) : a dictionary containing errors that occurred during the registration process.
    """

    __repository = UserRepository

    def __init__(self, data: Dict[str, str]) -> None:
        self.data = data
        self.__errors = {}

    @property
    def errors(self) -> Dict[str, str]:
        return self.__errors

    @errors.setter
    def errors(self, value: Dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError('The errors property must be a dictionary')
        self.__errors = value

    def __create(self, data: Dict[str, str]) -> None:
        """
        Tries to insert the user data into the repository.
        """

        if data.get('confirm_password', None):
            del data['confirm_password']
        try:
            self.__repository.insert(data)
        except self.__repository.UserRepositoryError as e:
            self.errors['code_error'] = 'database_error'
            self.errors['details'] = e.message
            raise

    def is_completed(self) -> bool:
        """
        Checks if the user registration is completed successfully.
        """

        try:
            self.__create(self.data)
            return True
        except self.__repository.UserRepositoryError:         
            return False
