from .connection import db_connection
from pymongo.collection import Collection
import abc


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


class MongoModel(abc.ABC):
    """
    Abstract base class for MongoDB models.

    This class provides a structure for defining MongoDB models with class-level properties for the collection name, schema validation, and indexes. It also provides a method for creating a MongoDB collection based on these properties.

    Attributes:
    - collection_name : The name of the MongoDB collection. Must be overridden in subclasses.
    - schema_validation : The validation schema for the MongoDB collection. Must be overridden in subclasses.
    - indexes : The indexes for the MongoDB collection. Must be overridden in subclasses.
    """
    
    @ClassProperty
    def name(cls):
        raise NotImplementedError(
            f'A name for the collection was not found in the {cls.__name__} class.'
        )

    @ClassProperty
    def schema_validation(cls):
        raise NotImplementedError(
            f'The validation scheme was not found for the {cls.name} collection.'
        )

    @ClassProperty
    def indexes(cls):
        raise NotImplementedError(
            f'Indexes were not found for the {cls.name} collection.'
        )
    
    @classmethod
    def get_collection_refer(cls) -> Collection:
        db = db_connection()
        if cls.name not in db.list_collection_names():
            raise Exception(f'Collection {cls.__name__} does not exist.')
        return db[cls.name]
    
    @classmethod
    def create_collection(cls) -> None:
        """
        Creates a new MongoDB collection with the name defined in the model if it does not exist. It also sets or modifies the validation schema for the collection and creates the indexes.
        """
        
        if not isinstance(cls.name, str):
            raise TypeError(f'{cls.name} must be a string')
        if not isinstance(cls.schema_validation, dict):
            raise TypeError(f'{cls.schema_validation} must be a dictionary')
        if not isinstance(cls.indexes, list):
            raise TypeError(f'{cls.indexes} must be a list')
        
        db = db_connection()
        if cls.name not in db.list_collection_names():
            try:
                # Create collection if it doesn't exist
                collection = db.create_collection(
                    name = cls.name,
                    validator = cls.schema_validation,
                    validationLevel = 'strict',
                )
                collection.create_indexes(cls.indexes)
            except Exception as e:
                db.client.close()
                raise Exception(f'Error creating collection {cls.name}: {e}')
            db.client.close()
        else:
            try:
                # Collection updated
                db.command(
                    command = 'collMod',
                    value = cls.name,
                    validator = cls.schema_validation,
                    validationLevel = 'strict',
                )
                db[cls.name].drop_indexes()
                db[cls.name].create_indexes(cls.indexes)
            except Exception as e:
                db.client.close()
                raise Exception(f'Error updating collection {cls.name}: {e}')
            db.client.close()