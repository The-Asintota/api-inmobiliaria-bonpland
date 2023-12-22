from typing import Optional, Dict, Any
from services.property.models.mongo_db import MongoModel
from services.property.models import Properties
from .abstract_repository import BaseRepository
from bson.objectid import ObjectId


class PropertyRepository(BaseRepository):
    """
    `PropertyRepository` is a class that encapsulates CRUD queries related to the `properties` collection.
    """

    __collection: MongoModel = Properties

    @classmethod
    def get_property_by_pk(cls, pk: ObjectId) -> Optional[Dict[str, Any]]:
        """
        Returns a property based on its primary key, if not found it returns None.
        """

        document = cls.__collection.get_collection_refer().find_one(
            {'pk': pk},
            projection={'_id': 0},
        )
        return cls.set_document(document) if document else None
