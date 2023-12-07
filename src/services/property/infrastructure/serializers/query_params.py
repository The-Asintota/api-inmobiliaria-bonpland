from typing import Any, List, Dict
from rest_framework import serializers
from django.core.validators import RegexValidator
from services.property.models.constants import PropertyType, LocalType, AvailabilityType


PRICE_REGEX = r"^(?:\d{1,5}(?:\.\d{1,2})?|300000)_(?:\d{1,5}(?:\.\d{1,2})?|300000)$"
ROOMS_BATHROOMS_FLOORS_REGEX = r"^(?:[1-5]|0_5)$"
INVALID_DATA_MESSAGE = 'Invalid data type.'


def validation_with_regex(regex, message):
    return RegexValidator(
        regex=regex,
        message=message,
        code='invalid_data',
    )


class QueryParamsSerializer(serializers.Serializer):
    """
    Serializer for validating and preparing query parameters.
    
    Attributes:
    - type_property (ListField): The property types to search in.
    - all (ListField): Boolean field indicating whether to search all properties.
    - availability_type (ListField): The types of availability to search for.
    - type_local (ListField): The types of local properties to search for.
    - parking_lot (ListField): Boolean field indicating whether to search for properties with a parking lot.
    - price_usd (ListField): The price range to search for properties in.
    - rooms (ListField): The number of rooms to search for.
    - bathrooms (ListField): The number of bathrooms to search for.
    - floors (ListField): The number of floors to search for.
    - garages (ListField): Boolean field indicating whether to search for properties with a garage.
    - garden (ListField): Boolean field indicating whether to search for properties with a garden.
    """
    
    type_property=serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                (PropertyType.HOME.value),
                (PropertyType.DEPARTMENT.value),
                (PropertyType.LOCAL.value),
            ],
        ),
        required=True,
    )
    all=serializers.ListField(
        child=serializers.BooleanField(),
        required=False,
    )
    availability_type=serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                (AvailabilityType.BUY.value),
                (AvailabilityType.RENT.value),
                (AvailabilityType.TEMPORARY_RENTAL.value),
            ],
        ),
        required=False,
    )
    type_local=serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                (LocalType.COMERCIAL.value),
                (LocalType.INDUSTRIAL.value),
            ],
        ),
        required=False,
    )
    parking_lot=serializers.ListField(
        child=serializers.BooleanField(),
        required=False,
    )
    price_usd=serializers.ListField(
        child=serializers.CharField(
            max_length=20,
            validators=[validation_with_regex(PRICE_REGEX, INVALID_DATA_MESSAGE)],
        ),
        required=False,
    )
    rooms=serializers.ListField(
        child=serializers.CharField(
            max_length=3,
            validators=[validation_with_regex(ROOMS_BATHROOMS_FLOORS_REGEX, INVALID_DATA_MESSAGE)],
        ),
        required=False,
    )
    bathrooms=serializers.ListField(
        child=serializers.CharField(
            max_length=3,
            validators=[validation_with_regex(ROOMS_BATHROOMS_FLOORS_REGEX, INVALID_DATA_MESSAGE)],
        ),
        required=False,
    )
    floors=serializers.ListField(
        child=serializers.CharField(
            max_length=3,
            validators=[validation_with_regex(ROOMS_BATHROOMS_FLOORS_REGEX, INVALID_DATA_MESSAGE)],
        ),
        required=False,
    )
    garages=serializers.ListField(
        child=serializers.BooleanField(),
        required=False,
    )
    garden=serializers.ListField(
        child=serializers.BooleanField(),
        required=False,
    )
    
    
    def validate_price_usd(self, value:List[str]) -> Dict[str, Any]:
        """
        Validate the price_usd field.
        """
        
        min_value, max_value = map(float, value[0].split('_'))
        if not  min_value < max_value and min_value != 0 and max_value != 0:
            raise serializers.ValidationError(
                detail='Minimum value must be less than maximum value.'
            )
        return value
    
    
    def validate(self, data:Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the query parameters.
        """
        
        if len(data)==1:
            raise serializers.ValidationError(
                detail='There must be at least two query parameters.'
            )
        return data