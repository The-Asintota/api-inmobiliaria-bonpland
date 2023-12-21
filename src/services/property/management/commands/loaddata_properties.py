from typing import Dict, Any, List
from django.core.management.base import BaseCommand
from services.property.models.constants import (
    PropertyType, AvailabilityType, LocalType
)
from services.property.models.mongo_db.connection import db_connection
from backend.settings.base import PROPERTY_COLLECTION
from bson import ObjectId, Decimal128
from faker import Faker
from datetime import datetime
import pytz
import random


fake = Faker('es_CO')
availability_type_values = [
    AvailabilityType.BUY.value,
    AvailabilityType.RENT.value,
]
type_local_values = [
    LocalType.COMERCIAL.value,
    LocalType.INDUSTRIAL.value,
]
objetc_field = {
    'count':2,
    'list': [
        '1', '2'
    ]
}


class Command(BaseCommand):
    """
    A Django management command that `creates` and inserts fake property data into a MongoDB collection.
    """

    help = 'Migrate collections.'

    def create_data(self) -> List[Dict[str, Any]]:
        """
        Creates a list of dictionaries, each representing a property with randomly generated data.
        """

        data = []
        i = 0
        while i < 20:
            data.append({
                'pk': ObjectId(),
                'short_description': fake.text(max_nb_chars=50),
                'long_description': fake.text(max_nb_chars=200),
                'type_property': PropertyType.HOME.value,
                'availability_type': random.choice(availability_type_values),
                'rooms': random.choice([3, 4, 5]),
                'bathrooms': random.choice([1, 2]),
                'floors': random.choice([1, 2, 3]),
                'ambient': objetc_field,
                'rules': objetc_field,
                'location': fake.address(),
                'garages': False,
                'garden': False,
                'extra_services': objetc_field,
                'covered_meters': Decimal128('420.50'),
                'discovered_meters': Decimal128('65.52'),
                'price_usd': Decimal128(
                    str(round(random.uniform(1000.00, 200000.00), 2))
                ),
                'date_joined': datetime.now(pytz.UTC)
            })
            data.append({
                'pk': ObjectId(),
                'short_description': fake.text(max_nb_chars=50),
                'long_description': fake.text(max_nb_chars=200),
                'type_property': PropertyType.DEPARTMENT.value,
                'availability_type': random.choice(availability_type_values),
                'rooms': random.choice([2, 3, 4]),
                'bathrooms': random.choice([1, 2]),
                'floors': random.choice([1, 2, 3]),
                'ambient': objetc_field,
                'rules': objetc_field,
                'location': fake.address(),
                'covered_meters': Decimal128('420.55'),
                'extra_services': objetc_field,
                'building_services': objetc_field,
                'price_usd': Decimal128(
                    str(round(random.uniform(1000.00, 200000.00), 2))
                ),
                'date_joined': datetime.now(pytz.UTC)
            })
            data.append({
                'pk': ObjectId(),
                'short_description': fake.text(max_nb_chars=50),
                'long_description': fake.text(max_nb_chars=200),
                'type_property': PropertyType.LOCAL.value,
                'availability_type': random.choice(availability_type_values),
                'type_local': random.choice(type_local_values),
                'extra_services': objetc_field,
                'use': objetc_field,
                'parking_lot': fake.pybool(),
                'location': fake.address(),
                'location_in': fake.address(),
                'price_usd': Decimal128(
                    str(round(random.uniform(1000.00, 200000.00), 2))
                ),
                'date_joined': datetime.now(pytz.UTC)
            })
            i += 1
        return data

    def handle(self, *args, **options) -> None:
        """
        Handles the execution of the command. It creates a connection to the MongoDB database, generates the data using the create_data method, and inserts it into the specified collection.
        """
        
        try:
            db = db_connection()
            db[PROPERTY_COLLECTION].insert_many(self.create_data())
        except Exception as e:
            db.client.close()
            print(e)
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created documents.'
                )
            )
            db.client.close()