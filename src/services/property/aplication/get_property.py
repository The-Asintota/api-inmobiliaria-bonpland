from typing import Optional, Dict, Any
from services.property.models.repository import PropertyRepository
from bson.objectid import ObjectId


class GetProperty:
    """
    `GetProperty` is a use case that uses the `PropertyRepository` class to retrieve a property based on its `primary key`.
    """
    
    __repository = PropertyRepository
    
    @classmethod
    def get_property(self, pk: str) -> Optional[Dict[str, Any]]:
        """
        Returns a `property` based on its `primary key`, if the property doesn't exist it returns `None`.
        """
        
        return self.__repository.get_property_by_pk(ObjectId(pk))