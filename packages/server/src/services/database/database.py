# @author: adibarra (Alec Ibarra)
# @description: Database class for handling database interactions

import importlib
import os

from config import POSTGRESQL_URI
from psycopg2 import pool

# Dynamic mixin loading
MIXINS_DIRECTORY = os.path.join(os.path.dirname(__file__), "mixins")
MIXINS_PACKAGE = "services.database.mixins"


def get_mixin_classes():
    """
    Retrieves all mixin classes from the mixins directory.
    """
    mixin_classes = []
    for filename in os.listdir(MIXINS_DIRECTORY):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{MIXINS_PACKAGE}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            class_name = filename[:-3].capitalize() + "Mixin"
            mixin_class = getattr(module, class_name, None)
            if mixin_class:
                mixin_classes.append(mixin_class)
    return mixin_classes


class Database(*get_mixin_classes(), object):
    """
    A class representing the database.
    """

    connectionPool: pool.SimpleConnectionPool = None

    def __new__(cls):
        """
        Creates a new instance of the Database class if it doesn't already exist.
        If an instance already exists, returns the existing instance.

        To see the available methods, refer to the mixin classes in the `services.database.mixins` package.

        Returns:
            Database: The Database instance.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
            try:
                print("Connecting to PostgreSQL database...")
                cls.instance.connectionPool = pool.SimpleConnectionPool(
                    1, 20, POSTGRESQL_URI
                )
                print("Connected to PostgreSQL database, connection pool created.")
            except Exception as e:
                print("Failed to connect to PostgreSQL database", e)

        return cls.instance

    def __init__(self):
        """
        Initializes a new instance of the Database class.

        This method establishes a connection to the PostgreSQL database and performs necessary setup tasks,
        such as creating the pgcrypto extension and initializing the required tables if they don't exist.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                # Create pgcrypto extension if it doesn't exist
                cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

                # Initialize necessary tables if they don't exist
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS users ("
                    + "  uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),"
                    + "  username TEXT NOT NULL,"
                    + "  email TEXT UNIQUE NOT NULL,"
                    + "  password_hash TEXT NOT NULL,"
                    + "  coins INT DEFAULT 10,"
                    + "  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,"
                    + "  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP"
                    + ");",
                )

                conn.commit()
                print("Database ready.")
        except Exception as e:
            print("Failed to connect to PostgreSQL database", e)
        finally:
            if conn:
                self.connectionPool.putconn(conn)
