from rest_framework.test import APITestCase
from test.test_property_services.factory import PropertyFactory
from backend.settings.base import PROPERTY_COLLECTION
from backend.settings.local import DATABASES
from pymongo import MongoClient
from decouple import config


class BaseTestCase(APITestCase):
    """
    BaseTestCase is a base test case class that sets up a MongoDB database for testing. It uses the PropertyFactory to generate test data and inserts it into the 'properties' collection.
    """

    factory = PropertyFactory

    @classmethod
    def setUpClass(cls):
        cls.mongo_client = MongoClient(
            host=DATABASES['mongo_db']['HOST'],
            port=DATABASES['mongo_db']['PORT'],
        )
        DATABASES['mongo_db']['NAME'] = config('MDB_NAME_TEST')
        cls.db = cls.mongo_client[config('MDB_NAME_TEST')]
        cls.collection = cls.db[PROPERTY_COLLECTION]

        i = 0
        while i < 20:
            cls.collection.insert_one(cls.factory.get_data_home())
            cls.collection.insert_one(cls.factory.get_data_department())
            cls.collection.insert_one(cls.factory.get_data_local())
            i += 1

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database(config('MDB_NAME_TEST'))
        DATABASES['mongo_db']['NAME'] = config('MDB_NAME_LOCAL')
