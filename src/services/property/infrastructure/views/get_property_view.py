from typing import Dict, Any
from rest_framework import (
    status, permissions, generics
)
from rest_framework.request import Request
from rest_framework.response import Response
from services.property.infrastructure.serializers import (
    PropertySerializer, GetPropertySerializer
)
from services.property.application import GetProperty
from services.property.schemas import get_property_schema


class GetPropertyAPIView(generics.RetrieveAPIView):
    """
    API view to `retrieve a property` based on its primary key (pk). This view handles GET requests and returns the property details in JSON format.
    """

    serializer_class = GetPropertySerializer
    permission_classes = (permissions.AllowAny,)
    application_class = GetProperty

    def _handle_valid_request(self, property: Dict[str, Any]) -> Response:
        """
        Handles the response for a valid request.
        """

        return Response(
            data=PropertySerializer(property).data,
            status=status.HTTP_200_OK,
            content_type='application/json',
        )

    def _handle_invalid_request(self, request_data: GetPropertySerializer) -> Response:
        """
        Handles the response for an invalid request.
        """

        return Response(
            data={
                'code_error': 'invalid_id',
                'details': request_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json',
        )

    @get_property_schema
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=kwargs)
        if not serializer.is_valid():
            return self._handle_invalid_request(serializer)
        property_object = self.application_class.get_property(
            pk=serializer.validated_data['pk']
        )
        if not property_object:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self._handle_valid_request(property_object)
