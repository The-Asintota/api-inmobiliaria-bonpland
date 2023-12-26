from rest_framework import serializers
from django.core.validators import (
    RegexValidator, MaxLengthValidator, MinLengthValidator
)


class AuthUserSerializer(serializers.Serializer):
    """
    Serializer for the authentication of users in the real estate management system.

    This serializer validates the user's email and password. The email is validated with a regex pattern and a maximum length constraint. The password is validated with a minimum length constraint.
    """

    email = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$",
                code='invalid_data',
            ),
            MaxLengthValidator(
                limit_value=100,
            )
        ]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={
            'input_type': 'password'
        },
        validators=[
            MinLengthValidator(
                limit_value=8,
            )
        ]
    )
