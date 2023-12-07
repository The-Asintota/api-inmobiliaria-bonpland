from typing import Any, Dict
from rest_framework import serializers


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