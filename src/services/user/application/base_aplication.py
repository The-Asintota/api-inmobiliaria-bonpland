from typing import Dict
from abc import ABC


class AbstractUseCase(ABC):
    """
    Use case that creates a user in the system.

    Attributes:
    - data (Dict[str, str]) : a dictionary containing user data for registration.
    - errors (Dict[str, str]) : a dictionary containing errors that occurred during the registration process.
    """

    def __init__(self, data: Dict[str, str]) -> None:
        self._data = data
        self._errors = {}

    @property
    def data(self) -> Dict[str, str]:
        return self._data

    @property
    def errors(self) -> Dict[str, str]:
        return self._errors

    @errors.setter
    def errors(self, value: Dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError('The errors property must be a dictionary')
        self._errors = value
