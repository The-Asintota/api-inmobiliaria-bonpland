from rest_framework import serializers
from bson import ObjectId


class PropertySerializer(serializers.Serializer):
    """
    Serializer for a `document` from the properties collection. This serializer is `read-only` and is used to serialize the data of a document property.\n
    Includes fields for all attributes of a Property.
    """
    
    pk = serializers.CharField(read_only=True)
    type_property = serializers.CharField(read_only=True)
    availability_type = serializers.CharField(read_only=True)
    short_description = serializers.CharField(read_only=True)
    long_description = serializers.CharField(read_only=True)
    type_local = serializers.CharField(read_only=True)
    extra_services = serializers.JSONField(read_only=True)
    building_services = serializers.JSONField(read_only=True)
    use = serializers.JSONField(read_only=True)
    rules = serializers.JSONField(read_only=True)
    ambient = serializers.JSONField(read_only=True)
    rooms = serializers.IntegerField(read_only=True)
    bathrooms = serializers.IntegerField(read_only=True)
    floors = serializers.IntegerField(read_only=True)
    covered_meters = serializers.CharField(read_only=True)
    discovered_meters = serializers.CharField(read_only=True)
    parking_lot = serializers.BooleanField(read_only=True)
    garages = serializers.BooleanField(read_only=True)
    garden = serializers.BooleanField(read_only=True)
    location = serializers.CharField(read_only=True)
    location_in = serializers.CharField(read_only=True)
    price_usd = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class ObjectIdField(serializers.Field):
    """
    Custom serializer field for handling MongoDB's `ObjectId`. This field is used to convert a string representation of an ObjectId into an actual ObjectId instance.\n
    If the string is not a valid ObjectId, it raises a ValidationError.
    """
    
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId format.")


class GetPropertySerializer(serializers.Serializer):
    """
    Serializer to get a property. This serializer is used to validate the `data needed` to obtain a document from the properties collection.\n
    Includes a field for the primary key (pk) of the Property, which is required.
    """
    
    pk=ObjectIdField(required=True)