from backend.settings.local import DATABASES
from pymongo.database import Database
from pymongo import MongoClient


def db_connection() -> Database:
    """
    Establishes a connection to a MongoDB database using the host, port, and database name specified in the environment variables.
    
    The environment variables are accessed using the `config` function from the `decouple` module.
    """

    try:
        client = MongoClient(
            host=DATABASES['mongo_db']['HOST'],
            port=DATABASES['mongo_db']['PORT'],
        )
        db = client[DATABASES['mongo_db']['NAME']]
    except Exception as e:
        raise e
    return db
