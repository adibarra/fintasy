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

    def create_session(self, owner: str) -> dict:
        """
        Creates a new session in the database.

        Args:
            owner (str): The uuid of the user.

        Returns:
            dict: A dictionary containing information about the newly created session if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sessions (owner) VALUES (%s) ON CONFLICT (owner) DO UPDATE SET token = DEFAULT RETURNING *",
                    (owner,),
                )
                session_data = cursor.fetchone()
                conn.commit()
                if session_data is not None:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, session_data))
                else:
                    print(
                        "Failed to retrieve session data after insertion.", flush=True
                    )
                    return None
        except psycopg2.IntegrityError as e:
            # Check if it's a duplicate key error
            if "duplicate key value violates unique constraint" in str(e):
                return None
            else:
                raise e
        except Exception as e:
            print("Failed to create session:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_session(self, token: str) -> bool:
        """
        Deletes a session from the database.

        Args:
            token (str): The token of the session.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM sessions WHERE token = %s", (token,))
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete session:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_session(self, token: str) -> str:
        """
        Retrieves the uuid of the session owner.

        Args:
            token (str): The token of the session.

        Returns:
            str: The uuid of the session owner if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT owner FROM sessions WHERE token = %s", (token,))
                uuid_user = cursor.fetchone()
                conn.commit()
                if uuid_user is not None:
                    return uuid_user[0]
                else:
                    return None
        except Exception as e:
            print("Failed to get session:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)
