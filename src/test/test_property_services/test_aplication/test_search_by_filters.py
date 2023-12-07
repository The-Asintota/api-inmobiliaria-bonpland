from typing import Dict, List
from services.property.models import Home, Department, Local
from test.test_property_services import BaseTestCase
from services.property.aplication import SearchProperty
from services.property.models.constants import (
    PropertyType, AvailabilityType, QueryParams, LocalType
)
from parameterized import parameterized


class TestSearchProperty(BaseTestCase):
    """
    This class contains unit tests for the SearchProperty application class.

    Attributes:
    - aplication_class (SearchProperty): An instance of the SearchProperty class that is being tested.
    """
    
    
    aplication_class=SearchProperty()
    
    
    def _assert_price_field(self, property_value, param_value:List[str]) -> None:
        """
        This method checks if the property value is within the specified price range.
        """
        
        min_value, max_value = map(float, param_value[0].split('_'))
        if min_value != 0 and max_value != 0:
            self.assertTrue(min_value <= property_value <= max_value)
        elif min_value == 0 and max_value != 0:
            self.assertTrue(property_value >= max_value)
        elif min_value != 0 and max_value == 0:
            self.assertTrue(property_value <= min_value)

    
    def _assert_integer_field(self, property_value:int, param_value:List[str]) -> None:
        """
        This method checks if the property value is within the specified integer range.
        """
        
        for value in param_value:
            if value.count('_'):
                min_value, max_value = value.split('_')
                self.assertTrue(property_value >= int(max_value))
            else:
                self.assertTrue(str(property_value) in param_value)
    
    
    def _assert_property(self, property, query_params:Dict[str, List[str]]) -> None:
        """
        This method checks if the property value matches the query parameters.
        """
        
        for param_name, param_value in query_params.items():
            if param_name in QueryParams.PRICE_FIELDS.value:
                self._assert_price_field(property[param_name], param_value)
            elif param_name in QueryParams.INTEGER_FIELDS.value:
                self._assert_integer_field(property[param_name], param_value)
            elif param_name in QueryParams.BOOLEAN_FIELDS.value:
                self.assertEqual(property[param_name], param_value[0])
            else:
                self.assertTrue(property[param_name] in param_value)
    
    
    @parameterized.expand(
        input=[({
                'type_property': [PropertyType.HOME.value],
                'availability_type': [AvailabilityType.RENT.value],
                'rooms': ['3'],
                'price_usd': ['199.00_256.00'],
                'garages': [False],
                'garden': [False],
            },),
            ({
                'type_property': [PropertyType.HOME.value],
                'availability_type': [AvailabilityType.BUY.value],
                'rooms': ['3'],
                'price_usd': ['0_150000.00'],
                'garden': [False],
            },),
            ({
                'type_property': [PropertyType.HOME.value],
                'availability_type': [AvailabilityType.TEMPORARY_RENTAL.value],
                'rooms': ['0_5'],
                'price_usd': ['2000.00_0'],
            },),
            ({
                'type_property': [PropertyType.HOME.value],
                'availability_type': [
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
                'rooms': ['3', '4'],
                'floors': ['1', '2'],
            },),
        ],
    )
    def test_search_in_home_model(self, query_params:Dict[str, List[str]]) -> None:
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self._assert_property(property, query_params)
    
    
    @parameterized.expand(
        input=[({
                'type_property':[PropertyType.DEPARTMENT.value],
                'availability_type':[AvailabilityType.RENT.value],
                'rooms':['3', '4'],
                'bathrooms':['1', '2'],
                'price_usd':['1000.00_1500.00'],
            },),
            ({
                'type_property':[PropertyType.DEPARTMENT.value],
                'availability_type':[AvailabilityType.BUY.value],
                'rooms':['2', '3'],
                'price_usd':['0_195000.00'],
            },),
            ({
                'type_property':[PropertyType.DEPARTMENT.value],
                'availability_type':[
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
                'rooms':['3', '4'],
                'bathrooms':['1', '2'],
            },),
        ],
    )
    def test_search_in_department_model(self, query_params:Dict[str, List[str]]) -> None:
        properties = self.aplication_class.get_properties(query_params.copy())        
        for property in properties:
            self._assert_property(property, query_params)
    
    
    @parameterized.expand(
        input=[({
                'type_property': [PropertyType.LOCAL.value],
                'type_local':[LocalType.COMERCIAL.value],
                'availability_type': [AvailabilityType.RENT.value],
                'parking_lot': [False],
                'price_usd': ['700.00_1500.00'],
            },),
            ({
                'type_property': [PropertyType.LOCAL.value],
                'type_local':[LocalType.INDUSTRIAL.value],
                'availability_type': [AvailabilityType.BUY.value],
                'parking_lot': [True],
                'price_usd': ['0_190000.00'],
            },),
            ({
                'type_property': [PropertyType.LOCAL.value],
                'availability_type': [
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
            },),
        ],
    )
    def test_search_in_local_model(self, query_params:Dict[str, List[str]]) -> None:
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self._assert_property(property, query_params)
    
    
    @parameterized.expand(
        input=[({
                'type_property':[
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                    PropertyType.LOCAL.value,
                ],
                'availability_type':[AvailabilityType.RENT.value],
                'price_usd':['1000.00_1500.00'],
            },),
            ({
                'type_property':[
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                ],
                'availability_type':[AvailabilityType.BUY.value],
                'rooms':['3'],
                'bathrooms':['1'],
            },),
        ],
    )
    def test_search_in_multiples_models(self, query_params:Dict[str, List[str]]) -> None:
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self._assert_property(property, query_params)
    
    
    @parameterized.expand(
        input=[({
                'type_property':[
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                    PropertyType.LOCAL.value,
                ],
                'all':[True]
            },),
        ],
    )
    def test_get_all_properties(self, query_params:Dict[str, List[str]]) -> None:
        total=Home.objects.count() + Department.objects.count() + Local.objects.count()
        properties = self.aplication_class.get_properties(query_params)
        self.assertEqual(len(properties), total)