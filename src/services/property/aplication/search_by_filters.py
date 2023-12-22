from typing import Any, Optional, List, Dict, Sequence
from services.property.models.repository import SearchRepository
from services.property.models.constants import QueryParams


class SearchProperty:
    """
    A class used to represent the use case of searching for properties based on specified filters.

    Attributes:
    - repository_class: SearchRepository an instance of the SearchRepository class.
    - field_types: dict a dictionary mapping field names to their types.
    """
    
    repository_class=SearchRepository
    field_types={
        **{field:'str' for field in QueryParams.STR_FIELDS.value},
        **{field:'integer' for field in QueryParams.INTEGER_FIELDS.value},
        **{field:'boolean' for field in QueryParams.BOOLEAN_FIELDS.value},
        **{field:'decimal' for field in QueryParams.DECIMAL_FIELDS.value},
    }
    
    def _process_field(self, field_type:str, value_list:List[str]) -> Dict[str, Any]:
        """
        Processes a field based on its type and a list of values.
        """
        
        if field_type == 'str':
            return {
                'type_query': 'multiple' if len(value_list) >= 2 else 'exact',
                'value': value_list if len(value_list) >= 2 else value_list[0]
            }
        elif field_type == 'integer':
            if len(value_list) == 1:
                return {
                    'type_query': 'gte' if value_list[0].count('_') else 'exact',
                    'value': int(value_list[0].split('_')[-1]) if value_list[0].count('_') else int(value_list[0]),
                }
            return {
                'type_query': 'multiple',
                'value': [int(n) for n in value_list],
            }
        elif field_type == 'boolean':
            return {
                'type_query': 'exact',
                'value': value_list[0],
            }
        elif field_type == 'decimal':
            min_value, max_value = map(float, value_list[0].split('_'))
            if min_value != 0 and max_value != 0:
                return {
                    'type_query': 'range',
                    'min_value': min_value,
                    'max_value': max_value,
                }
            elif min_value == 0 and max_value != 0:
                return {
                    'type_query': 'gte',
                    'value': max_value,
                }
            elif min_value != 0 and max_value == 0:
                return {
                    'type_query': 'lte',
                    'value': min_value,
                }
    
    def _process_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a dictionary of filters.
        """
        
        for key, value_list in filters.items():
            if key in self.field_types:
                filters[key] = self._process_field(self.field_types[key], value_list)
        
        return filters
    
    def get_properties(self, filters:Dict[str, Any]) -> Optional[List[Sequence[Dict]]]:
        """
        Retrieves properties based on the given data.
        """
        
        return self.repository_class.search(
            filters=self._process_filters(filters),
        )