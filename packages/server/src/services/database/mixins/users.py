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

    def create_user(self, username: str, email: str, password_hash: str) -> bool:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password_hash (str): The hashed password of the user.

        Returns:
            bool: True if the user was successfully created, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash),
                )
                conn.commit()
                return True
        except psycopg2.IntegrityError as e:
            # Check if it's a duplicate key error
            if "duplicate key value violates unique constraint" in str(e):
                return False
            else:
                raise e
        except Exception as e:
            print("Failed to create user:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_user_by_email(self, email: str) -> dict:
        """
        Retrieves a user from the database by email.

        Args:
            email (str): The email address of the user.

        Returns:
            dict: A dictionary representing the user if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
                if cursor.description:
                    column_names = [desc[0] for desc in cursor.description]
                    user = cursor.fetchone()
                    if user is not None:
                        return dict(zip(column_names, [str(value) for value in user]))
                    else:
                        print("User with email '%s' not found.", email)
                        return None
        except Exception as e:
            print("Failed to get user by email:", e)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)
