from typing import List, Sequence, Dict
from rest_framework import (
    generics, permissions, status
)
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import QueryParamsSerializer, PropertySerializer
from services.property.application import SearchProperty
from services.property.schemas import search_properties_schema


class SearchPropertyAPIView(generics.ListAPIView):
    """
    API view for `searching properties`. Inherits from ListAPIView which is a generic class-based view to handle the retrieval of a collection of instances.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = QueryParamsSerializer
    application_class = SearchProperty

    def __handle_valid_request(self, properties: List[Sequence[Dict]]) -> Response:
        """
        Handles the response for valid properties.
        """

        page = self.paginate_queryset(properties)
        paginated_response = self.get_paginated_response(page)
        pagination_data = paginated_response.data
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

    def __handle_invalid_request(self, request_data: QueryParamsSerializer) -> Response:
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

    @search_properties_schema
    def get(self, request: Request, *args, **kwargs) -> Response:
        request_data = self.serializer_class(data=request.query_params)
        if not request_data.is_valid():
            return self.__handle_invalid_request(request_data)
        properties = self.application_class.get_properties(
            request_data.validated_data)
        if not properties:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.__handle_valid_request(properties)
