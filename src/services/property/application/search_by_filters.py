from typing import Any, Optional, List, Dict, Sequence
from services.property.models.repository import SearchRepository
from services.property.models.constants import QueryParams


class SearchProperty:
    """
    A class used to represent the use case of searching for properties based on specified filters.
    """

    __repository_class = SearchRepository
    __field_types = {
        **{field: 'str' for field in QueryParams.STR_FIELDS.value},
        **{field: 'integer' for field in QueryParams.INTEGER_FIELDS.value},
        **{field: 'boolean' for field in QueryParams.BOOLEAN_FIELDS.value},
        **{field: 'decimal' for field in QueryParams.DECIMAL_FIELDS.value},
    }

    @classmethod
    def __process_string_field(cls, value: List[Sequence[str]]) -> Dict[str, Any]:
        """
        Processes a string field based on the given value.
        """

        return {
            'type_query': 'multiple' if len(value) >= 2 else 'exact',
            'value': value if len(value) >= 2 else value[0]
        }

    @classmethod
    def __process_integer_field(cls, value: List[Sequence[str]]) -> Dict[str, Any]:
        """
        Processes an integer field based on the given value.
        """

        if len(value) == 1:
            return {
                'type_query': 'gte' if value[0].count('_') else 'exact',
                'value': int(value[0].split('_')[-1]) if value[0].count('_') else int(value[0]),
            }
        return {
            'type_query': 'multiple',
            'value': [int(n) for n in value],
        }

    @classmethod
    def __process_boolean_field(cls, value: List[Sequence[str]]) -> Dict[str, Any]:
        """
        Processes a boolean field based on the given value.
        """

        return {
            'type_query': 'exact',
            'value': value[0],
        }

    @classmethod
    def __process_decimal_field(cls, value: List[Sequence[str]]) -> Dict[str, Any]:
        """
        Processes a decimal field based on the given value.
        """

        min_value, max_value = map(float, value[0].split('_'))
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

    @classmethod
    def __process_field(cls, field_type: str, value: List[Sequence[str]]) -> Dict[str, Any]:
        """
        Processes a field based on its type and a list of values.
        """

        FIELD_PROCESSORS = {
            'str': cls.__process_string_field,
            'integer': cls.__process_integer_field,
            'boolean': cls.__process_boolean_field,
            'decimal': cls.__process_decimal_field,
        }

        return FIELD_PROCESSORS[field_type](value)

    @classmethod
    def __process_filters(cls, filters: Dict[str, List[Sequence[str]]]) -> Dict[str, Any]:
        """
        Processes a dictionary of filters.
        """

        for field, value in filters.items():
            if field in cls.__field_types:
                filters[field] = cls.__process_field(
                    field_type=cls.__field_types[field],
                    value=value
                )

        return filters

    @classmethod
    def get_properties(cls, filters: Dict[str, Any]) -> Optional[List[Sequence[Dict]]]:
        """
        Retrieves properties based on the given data.
        """

        return cls.__repository_class.search(
            filters=cls.__process_filters(filters),
        )
