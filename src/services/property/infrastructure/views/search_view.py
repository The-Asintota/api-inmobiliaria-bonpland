from typing import List, Sequence, Dict
from rest_framework import (
    generics, permissions, status
)
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import QueryParamsSerializer, PropertySerializer
from services.property.aplication import SearchProperty


class SearchPropertyAPIView(generics.ListAPIView):
    """
    API view for searching properties. Inherits from ListAPIView which is a generic class-based view to handle the retrieval of a collection of instances.

    Attributes:
    - permission_classes: A tuple of permission classes the view should use.
    - serializer_class: The serializer class to be used.
    - aplication_class: An instance of the SearchProperty class.
    """
    
    permission_classes=(permissions.AllowAny,)
    serializer_class=QueryParamsSerializer
    aplication_class=SearchProperty()
    
    def _handle_valid_request(self, properties:List[Sequence[Dict]]) -> Response:
        """
        Handles the response for valid properties.
        """
        
        page=self.paginate_queryset(properties)
        paginated_response=self.get_paginated_response(page)
        pagination_data=paginated_response.data
        return Response(
            data={
                'count': pagination_data.get('count'),
                'next': pagination_data.get('next'),
                'previous': pagination_data.get('previous'),
                'results': PropertySerializer(instance=page, many=True).data,
            },
            status=status.HTTP_200_OK,
            content_type='application/json',
        )
    
    def _handle_invalid_request(self, request_data:QueryParamsSerializer) -> Response:
        """
        Handles the response for invalid request data.
        """
        
        return Response(
            data={
                'code_error': 'invalid_path_params',
                'details': request_data.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json',
        )
    
    def get(self, request:Request, *args, **kwargs) -> Response:
        """
        Handles GET requests. Validates the request data and returns the properties if valid, else returns an error.
        """
        
        request_data=self.serializer_class(data=request.query_params)
        if not request_data.is_valid():
            return self._handle_invalid_request(request_data)
        properties=self.aplication_class.get_properties(request_data.validated_data)
        if not properties:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self._handle_valid_request(properties)