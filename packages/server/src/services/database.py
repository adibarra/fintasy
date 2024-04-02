# @author: adibarra (Alec Ibarra)
# @description: Database class for handling database interactions

from enum import Enum

import psycopg2
from config import POSTGRESQL_URI


class Database(object):
    """
    A class representing a database connection.
    It is a singleton class.
    """

    ERROR_TYPES = Enum(
        "ERROR_TYPES",
        [
            "USER_EXISTS",
            "USER_NOT_FOUND",
            "USER_CREATION_FAILED",
        ],
    )

    ERROR_MESSAGES = {
        ERROR_TYPES.USER_EXISTS: "User with email already exists",
        ERROR_TYPES.USER_NOT_FOUND: "User not found",
        ERROR_TYPES.USER_CREATION_FAILED: "Failed to create user",
    }

    def __new__(cls):
        """
        Creates a new instance of the Database class if it doesn't already exist.

        Returns:
            Database: The instance of the Database class.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """
        This method creates necessary tables in the database if they don't already exist on startup.
        """

        connection = None
        try:
            print("Connecting to PostgreSQL database...")
            connection = psycopg2.connect(POSTGRESQL_URI)
            print("Connected to PostgreSQL database")
            cursor = connection.cursor()

            # create tables here if they don't exist

            connection.commit()

        except Exception as e:
            print("Failed to connect to PostgreSQL database", e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def create_user(self, username: str, email: str, password_hash: str) -> bool:
        """
        Attempts to create a new user in the database.

        Returns:
            bool: True if the user was created successfully, False otherwise.
        """

        connection = None
        try:
            connection = psycopg2.connect(POSTGRESQL_URI)
            cursor = connection.cursor()

            # check if user with email already exists
            # else create user

            connection.commit()
            return True

        except Exception:
            return False

        finally:
            if connection:
                cursor.close()
                connection.close()
