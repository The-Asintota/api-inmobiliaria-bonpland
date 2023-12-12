from typing import Any, Dict
from rest_framework import serializers
from services.property.models.constants import PropertyType
import copy


class PropertySerializer(serializers.Serializer):
    
    # Methods
    def to_representation(self, instance:Dict[str, Any]) -> Dict[str, Any]:
        data_copy= copy.copy(instance)
        property_id=data_copy.pop('id')
        short_description=data_copy.pop('short_description')
        long_description=data_copy.pop('long_description')
        type_property=data_copy.pop('type_property')
        del data_copy['date_joined']
        data={
            'id':property_id,
            'short_description':short_description,
            'long_description':long_description,
            'type_property':type_property,
            'features':data_copy,
        }
        return data


class GetPropertySerializer(serializers.Serializer):
    """
    Validate the data necessary to obtain a property.
    """
    
    pk=serializers.UUIDField(
        error_messages={
            'invalid':'Invalid property id.',
        },
        required=True,
    )
    type_property=serializers.ChoiceField(
        choices=[
            (PropertyType.HOME.value, PropertyType.HOME.value),
            (PropertyType.DEPARTMENT.value, PropertyType.DEPARTMENT.value),
            (PropertyType.LOCAL.value, PropertyType.LOCAL.value),
        ],
        error_messages={
            'invalid_choice':'Type property is not a valid choice.'
        },
        required=True,
    )