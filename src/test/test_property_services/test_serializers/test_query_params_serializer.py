from typing import Dict, List
from services.property.infrastructure.serializers import QueryParamsSerializer
from services.property.models.constants import (
    PropertyType, AvailabilityType, LocalType, QueryParams
)
from rest_framework.test import  APITestCase
from parameterized import parameterized


class TestQueryParamsSerializer(APITestCase):
    """
    This class contains unit tests for the QueryParamsSerializer class.

    Attributes:
    - serializer_class (QueryParamsSerializer): The class of the serializer to be tested.
    """


    serializer_class=QueryParamsSerializer   
    
    
    @parameterized.expand(
        input=[({
                'type_property':[
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                    PropertyType.LOCAL.value,
                ],
                'availability_type':[
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                    AvailabilityType.TEMPORARY_RENTAL.value,
                ],
                'type_local':[
                    LocalType.COMERCIAL.value,
                    LocalType.INDUSTRIAL.value,
                ],
                'rooms':['1', '2', '3', '4', '5', '0_5'],
                'bathrooms':['1', '2', '3', '4', '5', '0_5'],
                'floors':['1', '2', '3', '4', '5', '0_5'],
                'parking_lot':['true'],
                'garden':['true'],
                'garages':['true'],
                'all':['true'],
                'price_usd':['810.00_0'],
            },),
        ]
    )
    def test_serializer_is_valid(self, query_params:Dict[str, List[str]]) -> None :
        serializer=self.serializer_class(data=query_params)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.initial_data, query_params)
        for field, value in serializer.validated_data.items():
            if field in QueryParams.BOOLEAN_FIELDS.value:
                self.assertTrue(value[0] in [True, False])
                continue
            self.assertEqual(value, query_params[field])
    
    
    @parameterized.expand(
        input=[({
                'type_property':['home'],
                'availability_type':['buy'],
                'type_local':['commercial'],
                'rooms':['6'],
                'bathrooms':['6'],
                'floors':['6'],
                'parking_lot':['si'],
                'garden':['si'],
                'garages':['si'],
                'all':['si'],
                'price_usd':['0_-810.00'],
            },),
            ({
                'type_property':[1],
                'availability_type':[1],
                'type_local':[1],
                'rooms':['0'],
                'bathrooms':['0'],
                'floors':['0'],
                'price_usd':['price'],
            },),
            ({
                'rooms':['-1'],
                'bathrooms':['-1'],
                'floors':['-1'],
                'price_usd':['0_usd'],
            },),
        ]
    )
    def test_serializer_is_invalid(self, query_params:Dict[str, List[str]]) -> None :
        serializer=self.serializer_class(data=query_params)
        self.assertEqual(serializer.initial_data, query_params)
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        self.assertTrue(list(serializer.errors.keys()).sort() == list(query_params.keys()).sort())