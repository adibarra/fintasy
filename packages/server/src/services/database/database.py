# @author: adibarra (Alec Ibarra)
# @description: Database class for handling database interactions

from config import POSTGRESQL_URI
from psycopg2 import pool

# import all mixins here
from services.database.mixins.meta import MetaMixin
from services.database.mixins.portfolios import PortfolioMixin
from services.database.mixins.sessions import SessionsMixin
from services.database.mixins.tournaments import TournamentsMixin
from services.database.mixins.transactions import TransactionsMixin
from services.database.mixins.users import UsersMixin


# add all imported mixins here
class Database(
    MetaMixin,
    PortfolioMixin,
    SessionsMixin,
    TournamentsMixin,
    TransactionsMixin,
    UsersMixin,
    object,
):
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

                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS friends ("
                    + "  owner uuid DEFAULT gen_random_uuid(),"
                    + "  owner uuid NOT NULL"
                    + ");",
                )

                conn.commit()
                print("Database ready.")
        except Exception as e:
            print("Failed to connect to PostgreSQL database", e)
        finally:
            if conn:
                self.connectionPool.putconn(conn)
