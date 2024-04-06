# @author: adibarra (Alec Ibarra)
# @description: Database class for handling session database operations

from typing import TYPE_CHECKING

import psycopg2

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class SessionsMixin:
    """
    A collection of methods for handling session database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_session(self, uuid_user: str) -> dict:
        """
        Creates a new session in the database.

        Args:
            uuid_user (str): The uuid of the user.

        Returns:
            dict: A dictionary containing information about the newly created session if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sessions (uuid) VALUES (%s) ON CONFLICT (uuid) DO UPDATE SET token = DEFAULT RETURNING *",
                    (uuid_user,),
                )
                session_data = cursor.fetchone()
                if session_data is not None:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, session_data))
                else:
                    print("Failed to retrieve session data after insertion.")
                    return None
        except psycopg2.IntegrityError as e:
            # Check if it's a duplicate key error
            if "duplicate key value violates unique constraint" in str(e):
                return None
            else:
                raise e
        except Exception as e:
            print("Failed to create session:", e)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_session(self, uuid_user: str) -> bool:
        """
        Deletes a session from the database.

        Args:
            uuid_user (str): The uuid of user which owns the session.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM sessions WHERE uuid = %s", (uuid_user,))
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete session:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
