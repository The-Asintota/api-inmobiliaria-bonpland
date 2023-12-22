from typing import Dict, List, Any
from services.property.aplication import SearchProperty
from services.property.models.constants import (
    PropertyType, AvailabilityType, QueryParams, LocalType
)
from test.test_property_services import BaseTestCase
from parameterized import parameterized


class TestSearchProperty(BaseTestCase):
    """
    Test case for the `SearchProperty` application class.
    
    This class contains methods to test the functionality of the SearchProperty application class. It inherits from the BaseTestCase class.
    """
    
    aplication_class=SearchProperty()
    
    def __assert_price_field(self, property_value: str, param_value: List[str]) -> None:
        """
        Asserts that the price field of a property is within the specified range.
        
        Args:
        - property_value (str) : The price of the property.
        - param_value (List[str]) : The range of acceptable prices.
        """
        
        min_value, max_value = map(float, param_value[0].split('_'))
        if min_value != 0 and max_value != 0:
            self.assertTrue(min_value <= float(property_value) <= max_value)
        elif min_value == 0 and max_value != 0:
            self.assertTrue(float(property_value) >= max_value)
        elif min_value != 0 and max_value == 0:
            self.assertTrue(float(property_value) <= min_value)

    def __assert_integer_field(self, property_value: int, param_value: List[str]) -> None:
        """
        Asserts that an integer field of a property is within the specified range or matches the specified value.
        
        Args:
        - property_value (int) : The value of the property field.
        - param_value (List[str]) : The range of acceptable values or the specific acceptable value.
        """
        
        for value in param_value:
            if value.count('_'):
                min_value, max_value = value.split('_')
                self.assertTrue(property_value >= int(max_value))
            else:
                self.assertTrue(str(property_value) in param_value)
    
    def __assert_property(self, property: Dict[str, Any], query_params: Dict[str, List[str]]) -> None:
        """
        Asserts that a property matches the specified query parameters.
        
        Args:
        - property (Dict[str, Any]) : The property to test.
        - query_params (Dict[str, List[str]]) : The query parameters to match the property against.
        """
        
        for param_name, param_value in query_params.items():
            if param_name in QueryParams.DECIMAL_FIELDS.value:
                self.__assert_price_field(property[param_name], param_value)
            elif param_name in QueryParams.INTEGER_FIELDS.value:
                self.__assert_integer_field(property[param_name], param_value)
            elif param_name in QueryParams.BOOLEAN_FIELDS.value:
                self.assertEqual(property[param_name], param_value[0])
            else:
                self.assertTrue(property[param_name] in param_value)
    
    @parameterized.expand(
        input=[
            ({
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
    def test_search_home(self, query_params:Dict[str, List[str]]) -> None:
        """
        Tests the search functionality for home properties.
        
        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to use for the search.
        """
        
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self.__assert_property(property, query_params)
    
    @parameterized.expand(
        input=[
            ({
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
    def test_search_department(self, query_params:Dict[str, List[str]]) -> None:
        """
        Tests the search functionality for department properties.
        
        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to use for the search.
        """
        
        properties = self.aplication_class.get_properties(query_params.copy())        
        for property in properties:
            self.__assert_property(property, query_params)
    
    @parameterized.expand(
        input=[
            ({
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
    def test_search_local(self, query_params:Dict[str, List[str]]) -> None:
        """
        Tests the search functionality for local properties.
        
        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to use for the search.
        """
        
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self.__assert_property(property, query_params)
    
    @parameterized.expand(
        input=[
            ({
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
    def test_search_multiples_type_properties(self, query_params:Dict[str, List[str]]) -> None:
        """
        Tests the search functionality for multiple types of properties.
        
        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to use for the search.
        """
        
        properties = self.aplication_class.get_properties(query_params.copy())
        for property in properties:
            self.__assert_property(property, query_params)
    
    @parameterized.expand(
        input=[
            ({
                'all':[True]
            },),
        ],
    )
    def test_get_all_properties(self, query_params:Dict[str, List[str]]) -> None:
        """
        Tests the functionality to get all properties.
        
        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to use for the search.
        """
        
        total=self.collection.count_documents({})
        properties = self.aplication_class.get_properties(query_params)
        self.assertEqual(len(properties), total)