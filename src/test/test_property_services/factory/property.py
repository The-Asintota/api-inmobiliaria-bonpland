from typing import Dict, Any
from django.db.models import Model
from services.property.models import Home, Department, Local
from services.property.models.constants import (
    PropertyType, AvailabilityType, LocalType
)
from faker import Faker
from decimal import Decimal
import random


class PropertyFactory:
    """
    A factory class for creating property data for testing purposes.

    This class uses the Faker library to generate fake data and the random library to generate random choices and prices.
    It supports creating data for three types of properties: Home, Department, and Local.
    """
    
    _fake=Faker('es_CO')
    _model_home=Home
    _model_department=Department
    _model_local=Local
    availability_type_values=[
        AvailabilityType.BUY.value,
        AvailabilityType.RENT.value,
    ]
    type_local_values=[
        LocalType.COMERCIAL.value,
        LocalType.INDUSTRIAL.value,
    ]

    
    @property
    def fake(self):
        return self._fake
    
    
    @property
    def model_home(self):
        return self._model_home
    
    
    @property
    def model_department(self):
        return self._model_department
    
    
    @property
    def model_local(self):
        return self._model_local
    
    
    def _prices_for_homes(self, availability_type:str) -> float:
        """
        Generate a random price for a home based on its availability type.
        """
        
        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(140000.00, 200000.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(190.00, 400.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(200.00, 1000.00), 2)
    
    
    def _prices_for_departments(self, availability_type:str) -> float:
        """
        Generate a random price for a department based on its availability type.
        """
        
        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(190000.00, 299999.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(1000.00, 2000.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(2000.00, 4000.00), 2)
    
    
    def _prices_for_locals(self, availability_type:str) -> float:
        """
        Generate a random price for a local based on its availability type.
        """
        
        if availability_type == AvailabilityType.BUY.value:
            return round(random.uniform(180000.00, 299999.00), 2)
        elif availability_type == AvailabilityType.RENT.value:
            return round(random.uniform(700.00, 1500.00), 2)
        elif availability_type == AvailabilityType.TEMPORARY_RENTAL.value:
            return round(random.uniform(2000.00, 4000.00), 2)
    
    
    def get_data_home(self) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a home.
        """
        
        availability_type=random.choice(self.availability_type_values)
        return {
            'short_description':self.fake.text(max_nb_chars=50),
            'long_description':self.fake.text(max_nb_chars=200),
            'type_property':PropertyType.HOME.value,
            'availability_type':availability_type,
            'rooms':random.choice([3, 4, 5]),
            'bathrooms':random.choice([1, 2]),
            'floors':random.choice([1, 2, 3]),
            'ambient':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'rules':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'location':self.fake.address(),
            'garages':False,
            'garden':False,
            'extra_services':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'covered_meters':Decimal(round(random.uniform(0.01, 99.99), 2)),
            'discovered_meters':Decimal(round(random.uniform(0.01, 99.99), 2)),
            'price_usd':Decimal(self._prices_for_homes(availability_type))
        }
    
    
    def get_data_department(self) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a department.
        """
        
        availability_type=random.choice(self.availability_type_values)
        return {
            'short_description':self.fake.text(max_nb_chars=50),
            'long_description':self.fake.text(max_nb_chars=200),
            'type_property':PropertyType.DEPARTMENT.value,
            'availability_type':availability_type,
            'rooms':random.choice([2, 3, 4]),
            'bathrooms':random.choice([1, 2]),
            'floors':random.choice([1, 2, 3]),
            'ambient':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'rules':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'location':self.fake.address(),
            'covered_meters':Decimal(round(random.uniform(0.01, 99.99), 2)),
            'extra_services':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'building_services':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'price_usd':Decimal(self._prices_for_departments(availability_type))
        }
    
    
    def get_data_local(self) -> Dict[str, Any]:
        """
        Generate a dictionary of fake data for a local.
        """
        
        availability_type=random.choice(self.availability_type_values)
        return {
            'short_description':self.fake.text(max_nb_chars=50),
            'long_description':self.fake.text(max_nb_chars=200),
            'type_property':PropertyType.LOCAL.value,
            'availability_type':availability_type,
            'type_local':random.choice(self.type_local_values),
            'extra_services':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'use':self.fake.json(
                data_columns=[
                    ('count','pyint',{'min_value':0, 'max_value':9}),
                    ('list',[])
                ],
                num_rows=1
            ),
            'parking_lot':self.fake.pybool(),
            'location':self.fake.address(),
            'location_in':self.fake.address(),
            'price_usd':Decimal(self._prices_for_locals(availability_type))
        }
    
    
    def get_model_instance(self, type_property:str) -> Model:
        """
        Get the model class for a given property type.
        """
        
        models={
            PropertyType.HOME.value:self.model_home,
            PropertyType.DEPARTMENT.value:self.model_department,
            PropertyType.LOCAL.value:self.model_local
        }
        return models.get(type_property)
    
    
    def create_test_data(self) -> None:
        """
        Create test data for all types of properties. This method generates and save instances for each property type.
        """
        
        data_home=self.get_data_home()
        model=self.get_model_instance(PropertyType.HOME.value)
        model.objects.create(**data_home)
        data_department=self.get_data_department()
        model=self.get_model_instance(PropertyType.DEPARTMENT.value)
        model.objects.create(**data_department)
        data_local=self.get_data_local()
        model=self.get_model_instance(PropertyType.LOCAL.value)
        model.objects.create(**data_local)
    
    
    def create_home_instance(self, data:Dict[str, Any]) -> Model:
        """
        Create a home instance.
        """
        
        return self.model_home.objects.create(**data)
    
    
    def create_department_instance(self, data:Dict[str, Any]) -> Model:
        """
        Create a department instance.
        """
        
        return self.model_department.objects.create(**data)
    
    
    def create_local_instance(self, data:Dict[str, Any]) -> Model:
        """
        Create a local instance.
        """
        
        return self.model_local.objects.create(**data)