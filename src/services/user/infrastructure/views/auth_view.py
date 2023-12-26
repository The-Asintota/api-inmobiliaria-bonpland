from typing import Dict, Any
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from services.user.infrastructure.serializers import AuthUserSerializer
from services.user.application import UserAuthentication


class UserAuthAPIView(TokenObtainPairView):
    """
    User Authentication API View.

    This class handles the authentication requests for the real estate management system.
    It extends the TokenObtainPairView provided by the simplejwt package to handle JWT authentication.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthUserSerializer
    application_class = UserAuthentication

    def __handle_valid_request(self, request_data: Dict[str, Any]) -> Response:
        """
        Handles the response for a valid request.
        """

        auth = self.application_class(request_data)
        if auth.is_completed():
            return Response(
                data=auth.tokens,
                status=status.HTTP_200_OK,
                content_type='application/json',
            )
        return Response(
            data=auth.errors,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json',
        )

    def __handle_invalid_request(self, serializer: AuthUserSerializer) -> Response:
        """
        Handles the response for an invalid request.
        """

        return Response(
            data={
                'code_error': 'invalid_data',
                'details': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json',
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return self.__handle_valid_request(request_data=request.data)
        return self.__handle_invalid_request(serializer)
