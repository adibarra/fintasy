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

    def create_user(self, username: str, email: str, password_hash: str) -> dict:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password_hash (str): The hashed password of the user.

        Returns:
            dict: A dictionary containing information about the newly created user if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING *",
                    (username, email, password_hash),
                )
                user_data = cursor.fetchone()
                conn.commit()
                if user_data is not None:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, user_data))
                else:
                    print("Failed to retrieve user data after insertion.")
                    return None
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

    def get_user(self, uuid_user: str) -> dict:
        """
        Retrieves a user from the database by email or UUID.

        Args:
            uuid_user (str): The UUID of the user.

        Returns:
            dict: A dictionary representing the user if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE uuid = %s LIMIT 1", (uuid_user,)
                )
                if cursor.description:
                    user = cursor.fetchone()
                    if user is not None:
                        column_names = [desc[0] for desc in cursor.description]
                        return dict(zip(column_names, [str(value) for value in user]))
                    else:
                        print(f"User with uuid '{uuid_user}' not found.")
                        return None
        except Exception as e:
            print("Failed to get user by uuid:", e)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_user(
        self,
        uuid_user: str,
        email: str = None,
        username: str = None,
        password_hash: str = None,
    ) -> bool:
        """
        Updates a user in the database.

        Args:
            uuid_user (str): The UUID of the user.
            email (str, optional): The new email of the user.
            username (str, optional): The new username of the user.
            password_hash (str, optional): The new password hash of the user.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                set_clause = ""
                params = []

                if email is not None:
                    set_clause += " email = %s,"
                    params.append(email)
                if username is not None:
                    set_clause += " username = %s,"
                    params.append(username)
                if password_hash is not None:
                    set_clause += " password_hash = %s,"
                    params.append(password_hash)

                # Remove the trailing comma if any
                set_clause = set_clause.rstrip(",")

                query = f"UPDATE users SET {set_clause} WHERE uuid = %s"
                params.append(uuid_user)

                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print("Failed to update user:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_user(self, uuid_user: str) -> bool:
        """
        Deletes a user from the database.

        Args:
            uuid_user (str): The UUID of the user.

        Returns:
            bool: True if successful, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE uuid = %s", (uuid_user,))
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete user:", e)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
