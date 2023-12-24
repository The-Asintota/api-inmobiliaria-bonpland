from typing import Dict, Any
from rest_framework import (
    generics, permissions, status
)
from rest_framework.response import Response
from rest_framework.request import Request
from services.user.infrastructure.serializers import CreateUserSerializer
from services.user.application import RegisterUser
from services.user.schemas import register_user_schema


class RegisterUserAPIView(generics.GenericAPIView):
    """
    API View for registering a new user.

    This view handles the `POST` request to create a new user in the real estate management system. It uses the CreateUserSerializer to validate the incoming data and the RegisterUser application class to handle the actual registration process.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer
    application_class = RegisterUser

    def __handle_valid_request(self, data: Dict[str, Any]) -> Response:
        """
        Handles the response for a valid request.
        """

        register = self.application_class(data)
        if register.is_completed():
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            data=register.errors,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json',
        )

    def __handle_invalid_request(self, request_data: CreateUserSerializer) -> Response:
        """
        Handles the response for an invalid request.
        """

        return Response(
            data={
                'code_error': 'invalid_data',
                'details': request_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json',
        )

    @register_user_schema
    def post(self, request: Request, *args, **kwargs) -> Response:
        request_data = self.serializer_class(data=request.data)
        if request_data.is_valid():
            return self.__handle_valid_request(
                data=request_data.validated_data
            )
        return self.__handle_invalid_request(request_data)
