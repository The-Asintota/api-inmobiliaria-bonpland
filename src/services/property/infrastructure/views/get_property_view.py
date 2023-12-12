from rest_framework import (
    status, permissions, generics
)
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Model
from services.property.infrastructure.serializers import PropertySerializer, GetPropertySerializer
from services.property.models.repository import PropertyRepository


class GetPropertyAPIView(generics.RetrieveAPIView):
    
    serializer_class=GetPropertySerializer
    permission_classes=(permissions.AllowAny,)
    repository_class=PropertyRepository()
    
    
    def _handle_valid_request(self, property:Model) -> Response:
        return Response(
            data=PropertySerializer(property).data,
            status=status.HTTP_200_OK,
            content_type='application/json',
        )
    
    def _handle_invalid_request(self, request_data:GetPropertySerializer) -> Response:
        return Response(
            data={
                'code_error':'invalid_path_params',
                'details':request_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json',
        )
    
    def get(self, request:Request, *args, **kwargs) -> Response:
        serializer=self.serializer_class(data=kwargs)
        if not serializer.is_valid():
            return self._handle_invalid_request(serializer)
            
        property_object=self.repository_class.get_property(
            type_property=serializer.validated_data.get('type_property'),
            id=serializer.validated_data.get('pk'),
        )
        if not property_object:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self._handle_valid_request(property_object)
        