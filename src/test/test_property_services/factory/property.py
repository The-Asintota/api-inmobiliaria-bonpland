from typing import Dict, Any
from services.property.models.constants import (
    PropertyType, AvailabilityType, LocalType
)
from bson import ObjectId, Decimal128
from datetime import datetime
from faker import Faker
import random
import pytz


fake = Faker('es_CO')


class PropertyFactory:
    """
    A `factory class` for creating property data for testing purposes.

    This class uses the `Faker` library to generate fake data and the `random` library to generate random choices.
    """

    AVAILABILITY_TYPE_VALUES = [
        AvailabilityType.BUY.value,
        AvailabilityType.RENT.value,
    ]
    TYPE_LOCAL_VALUES = [
        LocalType.COMERCIAL.value,
        LocalType.INDUSTRIAL.value,
    ]
    OBJECT_FIELD = {
        'count': 2,
        'list': [
            '1', '2'
        ]
    }

    @classmethod
    def __prices_for_homes(cls, availability_type: str) -> float:
        """
        Generate a random price for a home based on its availability type.
        """

        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(140000.00, 200000.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(190.00, 400.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(200.00, 1000.00), 2)

    @classmethod
    def __prices_for_departments(cls, availability_type: str) -> float:
        """
        Generate a random price for a department based on its availability type.
        """

        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(190000.00, 299999.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(1000.00, 2000.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(2000.00, 4000.00), 2)

    @classmethod
    def __prices_for_locals(cls, availability_type: str) -> float:
        """
        Generate a random price for a local based on its availability type.
        """

        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(180000.00, 299999.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(700.00, 1500.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(2000.00, 4000.00), 2)

    @classmethod
    def get_data_home(cls, pk: str = None) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a home.
        """

        availability_type = random.choice(cls.AVAILABILITY_TYPE_VALUES)
        return {
            'pk': ObjectId(pk) if pk else ObjectId(),
            'short_description': fake.text(max_nb_chars=50),
            'long_description': fake.text(max_nb_chars=200),
            'type_property': PropertyType.HOME.value,
            'availability_type': availability_type,
            'rooms': random.choice([3, 4, 5]),
            'bathrooms': random.choice([1, 2]),
            'floors': random.choice([1, 2, 3]),
            'ambient': cls.OBJECT_FIELD,
            'rules': cls.OBJECT_FIELD,
            'location': fake.address(),
            'garages': False,
            'garden': False,
            'extra_services': cls.OBJECT_FIELD,
            'covered_meters': Decimal128(str(round(random.uniform(0.01, 99.99), 2))),
            'discovered_meters': Decimal128(str(round(random.uniform(0.01, 99.99), 2))),
            'price_usd': Decimal128(str(cls.__prices_for_homes(availability_type))),
            'date_joined': datetime.now(tz=pytz.UTC)
        }

    @classmethod
    def get_data_department(cls, pk: str = None) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a department.
        """

        availability_type = random.choice(cls.AVAILABILITY_TYPE_VALUES)
        return {
            'pk': ObjectId(pk) if pk else ObjectId(),
            'short_description': fake.text(max_nb_chars=50),
            'long_description': fake.text(max_nb_chars=200),
            'type_property': PropertyType.DEPARTMENT.value,
            'availability_type': availability_type,
            'rooms': random.choice([2, 3, 4]),
            'bathrooms': random.choice([1, 2]),
            'floors': random.choice([1, 2, 3]),
            'ambient': cls.OBJECT_FIELD,
            'rules': cls.OBJECT_FIELD,
            'location': fake.address(),
            'covered_meters': Decimal128(str(round(random.uniform(0.01, 99.99), 2))),
            'extra_services': cls.OBJECT_FIELD,
            'building_services': cls.OBJECT_FIELD,
            'price_usd': Decimal128(str(cls.__prices_for_departments(availability_type))),
            'date_joined': datetime.now(tz=pytz.UTC)
        }

    @classmethod
    def get_data_local(cls, pk: str = None) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a local.
        """

        availability_type = random.choice(cls.AVAILABILITY_TYPE_VALUES)
        return {
            'pk': ObjectId(pk) if pk else ObjectId(),
            'short_description': fake.text(max_nb_chars=50),
            'long_description': fake.text(max_nb_chars=200),
            'type_property': PropertyType.LOCAL.value,
            'availability_type': availability_type,
            'type_local': random.choice(cls.TYPE_LOCAL_VALUES),
            'extra_services': cls.OBJECT_FIELD,
            'use': cls.OBJECT_FIELD,
            'parking_lot': fake.pybool(),
            'location': fake.address(),
            'location_in': fake.address(),
            'price_usd': Decimal128(str(cls.__prices_for_locals(availability_type))),
            'date_joined': datetime.now(tz=pytz.UTC)
        }

    @classmethod
    def get_data(cls, pk: str = None) -> Dict[str, Any]:
        map_funcion = {
            PropertyType.HOME.value: lambda pk: cls.get_data_home(pk),
            PropertyType.DEPARTMENT.value: lambda pk: cls.get_data_department(pk),
            PropertyType.LOCAL.value: lambda pk: cls.get_data_local(pk),
        }
        type_property = random.choice([
            PropertyType.HOME.value,
            PropertyType.DEPARTMENT.value,
            PropertyType.LOCAL.value,
        ])
        pk = pk if pk else None
        return map_funcion[type_property](pk)
