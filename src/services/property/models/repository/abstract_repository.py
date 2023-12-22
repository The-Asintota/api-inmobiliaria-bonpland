from typing import Dict, Any
from services.property.models.constants import QueryParams
from bson.objectid import ObjectId
from datetime import datetime


class ClassProperty(property):
    """
    A descriptor that behaves as a property on both instances and classes.

    This class extends the built-in `property` class to allow properties to be used with classes
    in addition to instances. This is useful for creating properties on classes (class-level properties), similar to how `@classmethod` creates class-level methods.
    """

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        if self.getter is None:
            raise AttributeError("unreadable attribute")
        return self.getter(owner)


class BaseRepository:

    @ClassProperty
    def collection(cls):
        raise NotImplementedError(
            f'A name for the collection was not found in the {cls.__name__} class.'
        )

    @classmethod
    def set_document(cls, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set a value in a document by key.
        """

        for key, value in document.items():
            if key in QueryParams.DECIMAL_FIELDS.value:
                document[key] = str(value.to_decimal())
                continue
            elif isinstance(value, ObjectId):
                document[key] = str(value)
                continue
            elif isinstance(value, datetime):
                document[key] = value.isoformat()
                continue
        return document
