from typing import Optional
from django.db.models import Model
from services.property.models import Home,Department,Local
from services.property.models.constants import PropertyType


class PropertyRepository:
    """
    Encapsulates the CRUD operations of models Home, Department and Local.
    """
    
    _model_home=Home
    _model_department=Department
    _model_local=Local
    _model_fields={
        PropertyType.HOME.value:[field.name for field in _model_home._meta.get_fields()],
        PropertyType.DEPARTMENT.value:[field.name for field in _model_department._meta.get_fields()],
        PropertyType.LOCAL.value:[field.name for field in _model_local._meta.get_fields()],
    }
    
    
    def get_model_instance(self, type_property:str) -> Model:
        """
        Get the model class based on the type_property.
        """
        
        models={
            PropertyType.HOME.value:self._model_home,
            PropertyType.DEPARTMENT.value:self._model_department,
            PropertyType.LOCAL.value:self._model_local,
        }
        return models.get(type_property)
    
    
    def get_property(self, type_property:str, id:str) -> Optional[Model]:
        """
        Get a property by type and UID.
        """
        
        model=self.get_model_instance(type_property)
        return model.objects.filter(id=id).values().first()