from typing import Dict
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.core.validators import (
    RegexValidator, MaxLengthValidator, MinLengthValidator
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ErrorMessages(serializers.Serializer):
    """
    A serializer class that provides custom error messages for fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customized error messages
        msg = {
            'required': 'Este campo es requerido.',
            'blank': 'Este campo no puede estar en blanco.',
            'null': 'Este campo no puede ser nulo.',
        }
        fields = list(self.fields.keys())
        for field_name in fields:
            self.fields[field_name].error_messages.update(msg)


class CreateUserSerializer(ErrorMessages):
    """
    A serializer class for creating a new user.

    This class inherits from the ErrorMessages class which in turn inherits from the Serializer class of Django Rest Framework. It is designed to handle the serialization and validation of data for creating a new user.
    """

    email = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.values('email'),
                message="Este correo electrónico ya está en uso."
            ),
            RegexValidator(
                regex=r"^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$",
                message='Correo electrónico inválido.',
                code='invalid_data'
            ),
            MaxLengthValidator(
                limit_value=100,
                message='El valor ingresado supera el número máximo de caracteres permitidos (90).'
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
                message='El valor ingresado debe ser de al menos 8 caracteres'
            )
        ]
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={
            'input_type': 'password'
        }
    )

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError:
            if value.isdecimal():
                raise serializers.ValidationError(
                    detail='La contraseña debe contener al menos una mayuscula y una minuscula.',
                    code='Invalid_data'
                )
            raise serializers.ValidationError(
                detail='Esta contraseña es demasiado común.',
                code='Invalid_data'
            )
        return value

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
        password = data['password']
        confirm_password = data['confirm_password']
        if not password == confirm_password:
            raise serializers.ValidationError(
                detail='Las contraseñas no coinciden.',
                code='Invalid_data'
            )
        return data
