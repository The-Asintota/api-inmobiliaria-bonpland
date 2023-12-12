from typing import Any, Dict
from rest_framework import serializers
from services.property.models.constants import PropertyType


class PropertySerializer(serializers.Serializer):
    
    # Methods
    def to_representation(self, instance:Dict) -> Dict[str, Any]:
        property_id=instance.pop('id')
        short_description=instance.pop('short_description')
        long_description=instance.pop('long_description')
        type_property=instance.pop('type_property')
        del instance['date_joined']
        data={
            'id':property_id,
            'short_description':short_description,
            'long_description':long_description,
            'type_property':type_property,
            'features':instance,
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