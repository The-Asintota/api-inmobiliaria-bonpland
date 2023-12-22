from drf_spectacular.utils import (
    extend_schema, OpenApiResponse, OpenApiParameter, inline_serializer
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from services.property.models.constants import(
    PropertyType, AvailabilityType, LocalType
)


search_properties_schema=extend_schema(
    description='Busca inmuebles en el sistema según los _filtros de busqueda_ permitidos.',
    tags=['Inmuebles'],
    auth=[],
    parameters=[
        OpenApiParameter(
            name='type_property',
            description=f'Este filtro de búsqueda se usa para determinar el tipo de inmuble que se desea buscar, los valores possibles son:\n - {PropertyType.HOME.value}.\n - {PropertyType.LOCAL.value}.\n - {PropertyType.DEPARTMENT.value}.',
            type={
                'type': 'array',
                'items': {
                    'type':'string',
                }
            },
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='all',
            description='Este filtro de búsqueda se usa para obtener todos los inmuebles activos en el sistema.',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='availability_type',
            description=f'Este filtro de búsqueda se usa para definir la disponibilidad de un inmueble, los valores posibles son:\n - {AvailabilityType.BUY.value}.\n - {AvailabilityType.TEMPORARY_RENTAL.value}.\n - {AvailabilityType.RENT.value}.',
            type={
                'type': 'array',
                'items': {
                    'type':'string',
                }
            },
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='type_local',
            description=f'Este filtro de búsqueda se usa para definir el tipo de local, los valores posibles son:\n - {LocalType.COMERCIAL.value}.\n - {LocalType.INDUSTRIAL.value}.',
            type={
                'type': 'array',
                'items': {
                    'type':'string',
                }
            },
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='parking_lot',
            description='Este filtro de búsqueda se usa para determinar si un local debe tener acceso a parqueadero o no.',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='rooms',
            description='Este filtro de búsqueda se usa para definir el número de habitaciones del inmueble, los valores posibles son:\n - [1, 2, 3, 4, 5, 0_5].\n\n rooms=1  ==>  Exactamente una habitción.\n\n rooms=0_5  ==>  Más de cinco habitaciones.',
            type={
                'type': 'array',
                'items': {
                    'type':'string'
                }
            },
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='bathrooms',
            description='Este filtro de búsqueda se usa para definir el número de baños del inmueble, los valores posibles son:\n - [1, 2, 3, 4, 5, 0_5].\n\n bathrooms=1  ==>  Exactamente un baño.\n\n bathrooms=0_5  ==>  Más de cinco baños.',
            type={
                'type': 'array',
                'items': {
                    'type':'string',
                }
            },
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='floors',
            description='Este filtro de búsqueda se usa para definir el número de pisos del inmueble, los valores posibles son:\n - [1, 2, 3, 4, 5, 0_5].\n\n floors=1  ==>  Exactamente un piso.\n\n floors=0_5  ==>  Más de cinco pisos.',
            type={
                'type': 'array',
                'items': {
                    'type':'string',
                }
            },
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='garages',
            description='Este filtro se usa para determinar si un inmueble debe tener cochera o no.',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='garden',
            description='Este filtro se usa para determinar si un inmueble debe tener un jardín o no.',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='price_usd',
            description='Este filtro se usa para determinar el precio o rango de precios en el que debe estar un inmueble:\n1. **Consulta en rango:**\n  - price_usd=min_max  ==>  price_usd=0_150.50  ==>  Mayor a 150.50 dólares.\n  - price_usd=min_max  ==>  price_usd=589_0  ==>  Menor a 589 dólares.\n  - price_usd=min_max  ==>  price_usd=489.55_600.99  ==>  Entre 489.55 y 600.99 dólares.\n2. **Consulta exacta:**\n  - price_usd=value  ==>  price_usd=1540.80',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='page',
            description='Un número de página dentro del conjunto de resultados paginados.',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY
        )
    ],
    responses={
        200:OpenApiResponse(
            description='(OK) Retorna la lista de inmuebles que cumplen con los filtros de busqueda aplicados.',
            response=inline_serializer(
                name='Properties',
                fields={
                    'pk': serializers.CharField(
                        default='c7970c98-00c5-40fa-8587-f261c866e4a2'
                    ),
                    'short_description': serializers.CharField(
                        default='Apartamento de 2 dormitorios en el centro de la ciudad.'
                    ),
                    'type_property': serializers.CharField(
                        default=PropertyType.HOME.value
                    ),
                    "availability_type":serializers.CharField(
                        default=AvailabilityType.BUY.value
                    ),
                    "rooms":serializers.IntegerField(
                        default=3
                    ),
                    "bathrooms":serializers.IntegerField(
                        default=2
                    ),
                    "floors":serializers.IntegerField(
                        default=2
                    ),
                    "location":serializers.CharField(
                        default='Mar del Plata 7655, Buenos Aires'
                    ),
                    "covered_meters":serializers.IntegerField(
                        default=200
                    ),
                    "discovered_meters":serializers.IntegerField(
                        default=240
                    ),
                    "price_usd":serializers.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        min_value=0,
                        default=100.55
                    )
                },
                many=True
            )
        ),
        404:OpenApiResponse(
            description='(NOT_FOUND) No se encontraron inmuebles que cumplan con los filtros aplicados.'
        ),
        400:OpenApiResponse(
            description='(BAD_REQUEST) La petición no es válida por alguna de las siguientes razones:\n- Parámetros de consulta inválidos.\n',
            response={
                "properties":{
                    "code_error":{
                        "type":"string",
                        "example":"invalid_path_params"
                    },
                    "details":{
                        "type":"object",
                        "properties":{
                            "bathrooms":{
                                "type":"object",
                                "properties":{
                                    "0":{
                                        "type":"array",
                                        "items":{
                                            "type":"string"
                                        },
                                        "example":[
                                            "Invalid path params."
                                        ]
                                    },
                                }
                            },
                        }
                    },
                }
            }
        )
    }
)