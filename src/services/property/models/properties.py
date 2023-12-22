from services.property.models.constants import PropertyType, AvailabilityType, LocalType
from .mongo_db.collection import MongoModel
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT


SCHEMA_OBJECT = {
    "bsonType": "object",
    "description": "must be an object and is required",
    "required": ["count", "list"],
    "properties": {
        "count": {
            "bsonType": "int",
            "maxLength": 2,
            "description": "must be an int and is required"
        },
        "list": {
            "bsonType": "array",
            "maxItems": 99,
            "description": "must be an array and is required"
        }
    }
}


class Properties(MongoModel):

    name = 'properties'
    schema_validation = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["pk", "type_property", "availability_type", "short_description", "long_description", "location", "price_usd", "date_joined"],
            "properties": {
                "pk": {
                    "bsonType": "objectId",
                    "description": "must be an objectId and is required"
                },
                "type_property": {
                    "enum": [
                        PropertyType.HOME.value,
                        PropertyType.DEPARTMENT.value,
                        PropertyType.LOCAL.value,
                    ],
                    "description": "must be a string and is required"
                },
                "availability_type": {
                    "enum": [
                        AvailabilityType.BUY.value,
                        AvailabilityType.RENT.value,
                        AvailabilityType.TEMPORARY_RENTAL.value
                    ],
                    "description": "must be a string and is required"
                },
                "short_description": {
                    "bsonType": "string",
                    "maxLength": 100,
                    "description": "must be a string and is required"
                },
                "long_description": {
                    "bsonType": "string",
                    "maxLength": 500,
                    "description": "must be a string and is required"
                },
                "type_local": {
                    "enum": [
                        LocalType.COMERCIAL.value,
                        LocalType.INDUSTRIAL.value
                    ],
                    "description": "must be a string and is required"
                },
                "extra_services": SCHEMA_OBJECT,
                "building_services": SCHEMA_OBJECT,
                "use": SCHEMA_OBJECT,
                "rules": SCHEMA_OBJECT,
                "ambient": SCHEMA_OBJECT,
                "rooms": {
                    "bsonType": "int",
                    "maxLength": 2,
                    "description": "must be an int and is required"
                },
                "bathrooms": {
                    "bsonType": "int",
                    "maxLength": 2,
                    "description": "must be an int and is required"
                },
                "floors": {
                    "bsonType": "int",
                    "maxLength": 2,
                    "description": "must be an int and is required"
                },
                "covered_meters": {
                    "bsonType": "decimal",
                    "description": "must be a decimal and is required"
                },
                "discovered_meters": {
                    "bsonType": "decimal",
                    "description": "must be a decimal and is required"
                },
                "parking_lot": {
                    "bsonType": "bool",
                    "description": "must be a boolean and is required"
                },
                "garages": {
                    "bsonType": "bool",
                    "description": "must be a boolean and is required"
                },
                "garden": {
                    "bsonType": "bool",
                    "description": "must be a boolean and is required"
                },
                "location": {
                    "bsonType": "string",
                    "maxLength": 100,
                    "description": "must be a string and is required"
                },
                "location_in": {
                    "bsonType": "string",
                    "maxLength": 100,
                    "description": "must be a string and is required"
                },
                "price_usd": {
                    "bsonType": "decimal",
                    "description": "must be a decimal and is required"
                },
                "date_joined": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                },
            }
        }
    }
    indexes = [
        IndexModel(
            [
                ('pk', ASCENDING)
            ],
            name='pk_field_index',
            unique=True
        ),
        IndexModel(
            [
                ('type_property', TEXT),
                ('availability_type', TEXT),
                ('type_local', TEXT),
            ],
            name='text_type_field_indexes'
        ),
        IndexModel(
            [
                ('rooms', ASCENDING),
                ('bathrooms', ASCENDING),
                ('floors', ASCENDING),
            ],
            name='int_type_field_indexes'
        ),
        IndexModel(
            [
                ('garden', ASCENDING),
                ('garages', ASCENDING),
                ('parking_lot', ASCENDING),
            ],
            name='boolean_type_field_indexes'
        ),
        IndexModel(
            [
                ('price_usd', DESCENDING),
            ],
            name='decimal_type_field_indexes'
        ),
    ]
