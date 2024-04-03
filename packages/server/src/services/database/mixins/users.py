# @author: adibarra (Alec Ibarra)
# @description: Database class for handling user database operations

from typing import TYPE_CHECKING

import psycopg2

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class UsersMixin:
    """
    A collection of methods for handling user database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_user(self, username: str, email: str, password_hash: str) -> str:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password_hash (str): The hashed password of the user.

        Returns:
            uuid (str): The UUID of the newly created user if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING uuid",
                    (username, email, password_hash),
                )
                uuid = cursor.fetchone()[0]
                conn.commit()
                return uuid
        except psycopg2.IntegrityError as e:
            # Check if it's a duplicate key error
            if "duplicate key value violates unique constraint" in str(e):
                return None
            else:
                raise e
        except Exception as e:
            print("Failed to create user:", e)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_user(self, uuid: str) -> dict:
        """
        Retrieves a user from the database by email or UUID.

        Args:
            uuid (str): The UUID of the user.

        Returns:
            dict: A dictionary representing the user if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE uuid = %s LIMIT 1", (uuid,))
                if cursor.description:
                    column_names = [desc[0] for desc in cursor.description]
                    user = cursor.fetchone()
                    if user is not None:
                        return dict(zip(column_names, [str(value) for value in user]))
                    else:
                        print(f"User with uuid '{uuid}' not found.")
                        return None
        except Exception as e:
            print("Failed to get user by uuid:", e)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_user(self, uuid: str, **kwargs) -> bool:
        """
        Updates a user in the database.

        Args:
            uuid (str): The UUID of the user.
            **kwargs: The fields to update.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
                query = f"UPDATE users SET {set_clause} WHERE uuid = %s"
                values = list(kwargs.values()) + [uuid]
                cursor.execute(query, values)
                conn.commit()
                return True
        except Exception as e:
            print("Failed to update user:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_user(self, uuid: str) -> bool:
        """
        Deletes a user from the database.

        Args:
            uuid (str): The UUID of the user.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE uuid = %s", (uuid,))
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete user:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
