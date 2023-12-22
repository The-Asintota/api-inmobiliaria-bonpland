from drf_spectacular.utils import (
    extend_schema, OpenApiResponse, OpenApiParameter, inline_serializer
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from services.property.models.constants import PropertyType, AvailabilityType


get_property_schema = extend_schema(
    description='_Obtiene toda la información_ de un inmueble en el sistema según su id.',
    tags=['Inmuebles'],
    auth=[],
    parameters=[
        OpenApiParameter(
            name='id',
            description='Identificador unico de un inmueble.',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description='(OK) Retorna la información del inmueble solicitado.',
            response=inline_serializer(
                name='Property',
                fields={
                    'pk': serializers.CharField(
                        default='c7970c98-00c5-40fa-8587-f261c866e4a2'
                    ),
                    'short_description': serializers.CharField(
                        default='Apartamento de 2 dormitorios en el centro de la ciudad.'
                    ),
                    'long_description': serializers.CharField(
                        default='Apartamento de 2 dormitorios en el centro de la ciudad.'
                    ),
                    'type_property': serializers.CharField(
                        default=PropertyType.HOME.value
                    ),
                    "availability_type": serializers.CharField(
                        default=AvailabilityType.BUY.value
                    ),
                    "rooms": serializers.IntegerField(
                        default=3
                    ),
                    "bathrooms": serializers.IntegerField(
                        default=2
                    ),
                    "floors": serializers.IntegerField(
                        default=2
                    ),
                    "ambient": serializers.JSONField(
                        default={
                            "count": 2,
                            "list": ["Ambiente 1", "Ambiente 2"]
                        }
                    ),
                    "rules": serializers.JSONField(
                        default={
                            "count": 3,
                            "list": ["Regla 1", "Regla 2", "Regla 3"]
                        }
                    ),
                    "location": serializers.CharField(
                        default='Mar del Plata 7655, Buenos Aires'
                    ),
                    "garage": serializers.IntegerField(
                        default=2
                    ),
                    "garden": serializers.BooleanField(
                        default=False
                    ),
                    "extra_services": serializers.JSONField(
                        default={
                            "count": 2,
                            "list": ["Servicio 1", "Servicio 2"]
                        }
                    ),
                    "covered_meters": serializers.IntegerField(
                        default=200
                    ),
                    "discovered_meters": serializers.IntegerField(
                        default=240
                    ),
                    "price_usd": serializers.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        min_value=0,
                        default=100.55
                    )
                }
            )
        ),
        404: OpenApiResponse(
            description='(NOT_FOUND) No se encontraron inmuebles que cumplan con los filtros aplicados.'
        ),
        400: OpenApiResponse(
            description='(BAD_REQUEST) La petición no es válida por alguna de las siguientes razones:\n- Id inválido.',
            response={
                "properties": {
                    "code_error": {
                        "type": "string",
                        "example": "invalid_id"
                    },
                    "details": {
                        "type": "object",
                        "properties": {
                            "pk": {
                                "type": "string",
                                "example": "Invalid ObjectId format."
                            }
                        }
                    }
                }
            }
        )
    }
)
