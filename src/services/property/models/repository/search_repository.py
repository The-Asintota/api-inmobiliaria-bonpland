from typing import Optional, List, Dict, Sequence, Any
from .. import Home, Department, Local
from ..constants import PropertyType
from django.db import connection
from django.db.models import Q, Model


class SearchRepository:
    """
    A repository for managing search operations on Home, Department, and Local models.

    This class provides methods to get model instances, construct query conditions, and perform queries 
    on the models based on provided filters.
    
    Attributes:
    - model_home: The Home model.
    - model_department: The Department model.
    - model_local: The Local model.
    - model_fields: A dictionary mapping property types to their corresponding fields.
    """
    
    model_home=Home
    model_department=Department
    model_local=Local
    model_fields={
        PropertyType.HOME.value:[field.name for field in model_home._meta.get_fields()],
        PropertyType.DEPARTMENT.value:[field.name for field in model_department._meta.get_fields()],
        PropertyType.LOCAL.value:[field.name for field in model_local._meta.get_fields()],
    }

    def get_model_instance(self, type_property:PropertyType) -> Model:
        """
        Returns the model instance based on the type of property.
        """
        
        models = {
            PropertyType.HOME.value:self.model_home,
            PropertyType.DEPARTMENT.value:self.model_department,
            PropertyType.LOCAL.value:self.model_local,
        }
        return models[type_property]

    def get_query_condition(self, filters:Dict[str, Any]) -> Q:
        """
        Constructs a query condition based on the provided filters.
        """
        
        query_types = {
            'range':lambda field, value:Q(**{f'{field}__range':(value['min_value'], value['max_value'])}),
            'lte':lambda field, value:Q(**{f'{field}__lte':value['value']}),
            'gte':lambda field, value:Q(**{f'{field}__gte':value['value']}),
            'exact':lambda field, value:Q(**{field:value['value']}),
            'multiple':lambda field, value:Q(**{f'{field}__in':value['value']}),
        }
        
        conditions = Q()
        for field, value in filters.items():
            type_query = value['type_query']
            conditions &= query_types[type_query](field, value)
        return conditions
    
    def query(self, filters:Dict[str, Dict],
              type_property:PropertyType,
              get_all:bool) -> Optional[List[Sequence[Dict]]]:
        """
        Performs a query with filters on a specific model.
        """
        
        clean_filters=dict()
        for key, value in filters.items():
            if key in self.model_fields[type_property]:
                clean_filters[key]=value
        model=self.get_model_instance(type_property)
        if get_all:
            return model.objects.all().values()
        return list(model.objects.filter(self.get_query_condition(clean_filters)).values())

    def search(self, search_in:List[PropertyType],
               filters:Dict[str, Any]) -> Optional[List[Sequence[Dict]]]:
        """
        Performs a search operation with filters on a specific model.
        """
        
        # Check if the database connection is working
        try:
            connection.ensure_connection()
        except Exception:
            return None
        query_set = []
        for type_property in search_in:
            properties = self.query(
                filters=filters,
                type_property=type_property,
                get_all=filters.get('all', False),
            )
            query_set.extend(properties)
        return sorted(query_set, key=lambda property: property['date_joined'], reverse=True)