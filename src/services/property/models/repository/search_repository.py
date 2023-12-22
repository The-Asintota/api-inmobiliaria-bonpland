from typing import Optional, List, Dict
from services.property.models.mongo_db import MongoModel
from services.property.models import Properties
from .base_repository import BaseRepository


class SearchRepository(BaseRepository):
    """
    A repository class for handling search operations on Properties collection.
    """
    
    collection: MongoModel = Properties
    __map_query_types = {
        'range': lambda field, value: {field: {'$gte': value['max_value'], '$lte': value['min_value']}},
        'lte': lambda field, value: {field: {'$lte': value['value']}},
        'gte': lambda field, value: {field: {'$gte': value['value']}},
        'exact': lambda field, value: {field: value['value']},
        'multiple': lambda field, value: {field: {'$in': value['value']}},
    }
    
    @classmethod
    def __query(cls, filters: Dict[str, Dict], get_all: bool) -> Optional[List[Dict]]:
        """
        Execute a search query on the Properties collection..

        Args:
        - filters (Dict[str, Dict]) : The filters to apply to the query.
        - get_all (bool) : Whether to return all documents.
        """
        
        if get_all:
            cursor = cls.collection.get_collection_refer().find({})
            return [doc for doc in cursor]
        query = {}
        for field, value in filters.items():
            query.update(cls.__map_query_types[value['type_query']](field, value))
        cursor = cls.collection.get_collection_refer().find(
            filter=query,
            projection={'_id': 0},
        ).sort('date_joined', -1)
        return [cls.set_document(doc) for doc in cursor]

    @classmethod
    def search(cls, filters:Dict[str, List]) -> Optional[List]:
        """
        Searches the Properties collection using the provided filters.
        """
        
        properties = cls.__query(
            filters=filters,
            get_all=filters.get('all', False),
        )
        return properties