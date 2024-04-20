# @author: adibarra (Alec Ibarra)
# @description: Database class for handling tournament database operations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class TournamentsMixin:
    """
    A collection of methods for handling tournament database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_tournament(
        self, owner: str, name: str, start_date: str, end_date: str
    ) -> dict:
        """
        Creates a new tournament in the database.

        Args:
            owner (str): The UUID of the tournament owner.
            name (str): The name of the tournament.
            start_date (str): The start date of the tournament.
            end_date (str): The end date of the tournament.

        Returns:
            dict: A dictionary representing the created tournament if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tournaments (owner, name, start_date, end_date) VALUES (%s, %s, %s, %s) RETURNING *",
                    (owner, name, start_date, end_date),
                )
                tournament = cursor.fetchone()
                conn.commit()
                if tournament is not None:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, tournament))
                else:
                    print("Failed to retrieve the created tournament.", flush=True)
                    return None
        except Exception as e:
            print("Failed to create tournament:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_tournament(
        self,
        uuid_tournament: str,
        name: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> bool:
        """
        Updates a tournament in the database by UUID.

        Args:
            uuid_tournament (str): The UUID of the tournament to update.
            name (str, optional): The new name of the tournament.
            start_date (str, optional): The new start date of the tournament.
            end_date (str, optional): The new end date of the tournament.

        Returns:
            bool: True if the tournament was successfully updated, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                query = "UPDATE tournaments SET"
                params = []
                if name is not None:
                    query += " name = %s,"
                    params.append(name)
                if start_date is not None:
                    query += " start_date = %s,"
                    params.append(start_date)
                if end_date is not None:
                    query += " end_date = %s,"
                    params.append(end_date)

                # Remove the trailing comma if any
                query = query.rstrip(",")

                # Add the WHERE clause for UUID
                query += " WHERE uuid = %s"
                params.append(uuid_tournament)

                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print("Failed to update tournament by UUID:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_tournament(self, uuid_tournament: str) -> bool:
        """
        Deletes a tournament from the database by UUID.

        Args:
            uuid_tournament (str): The UUID of the tournament to delete.

        Returns:
            bool: True if the tournament was successfully deleted, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tournaments WHERE uuid = %s", (uuid_tournament,)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete tournament by UUID:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_tournament(self, uuid_tournament: str) -> dict:
        """
        Retrieves a tournament from the database by UUID.

        Args:
            uuid_tournament (str): The UUID of the tournament.

        Returns:
            dict: A dictionary representing the tournament if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM tournaments WHERE uuid = %s LIMIT 1",
                    (uuid_tournament,),
                )
                if cursor.description:
                    tournament = cursor.fetchone()
                    if tournament is not None:
                        column_names = [desc[0] for desc in cursor.description]
                        return dict(zip(column_names, tournament))
        except Exception as e:
            print("Failed to get tournament by UUID:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_tournaments(
        self,
        owner: str = None,
        name: str = None,
        status: str = None,
        start_date: str = None,
        start_date_before: str = None,
        start_date_after: str = None,
        end_date: str = None,
        end_date_before: str = None,
        end_date_after: str = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[dict]:
        """
        Retrieve tournaments from the database based on the provided filters.

        Args:
            owner (str, optional): The UUID of the tournament owner. Defaults to None.
            name (str, optional): The name of the tournament. Defaults to None.
            status (str, optional): The status of the tournament. Defaults to None.
            start_date (str, optional): The start date of the tournament. Defaults to None.
            start_date_before (str, optional): The upper bound for the start date of the tournament. Defaults to None.
            start_date_after (str, optional): The lower bound for the start date of the tournament. Defaults to None.
            end_date (str, optional): The end date of the tournament. Defaults to None.
            end_date_before (str, optional): The upper bound for the end date of the tournament. Defaults to None.
            end_date_after (str, optional): The lower bound for the end date of the tournament. Defaults to None.
            offset (int, optional): The number of records to skip. Defaults to 0.
            limit (int, optional): The maximum number of records to retrieve. Defaults to 10.

        Returns:
            List[dict]: A list of dictionaries representing the retrieved tournaments.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                query = "SELECT * FROM tournaments WHERE TRUE"
                params = []

                if owner is not None:
                    query += " AND owner = %s"
                    params.append(owner)
                if name is not None:
                    query += " AND name = %s"
                    params.append(name)
                if status is not None:
                    query += " AND status = %s"
                    params.append(status)
                if start_date is not None:
                    query += " AND start_date = %s"
                    params.append(start_date)
                if start_date_before is not None:
                    query += " AND start_date < %s"
                    params.append(start_date_before)
                if start_date_after is not None:
                    query += " AND start_date > %s"
                    params.append(start_date_after)
                if end_date is not None:
                    query += " AND end_date = %s"
                    params.append(end_date)
                if end_date_before is not None:
                    query += " AND end_date < %s"
                    params.append(end_date_before)
                if end_date_after is not None:
                    query += " AND end_date > %s"
                    params.append(end_date_after)

                query += " OFFSET %s LIMIT %s"
                params.extend([offset, limit])

                cursor.execute(query, params)
                column_names = [desc[0] for desc in cursor.description]
                tournaments = [
                    dict(zip(column_names, row)) for row in cursor.fetchall()
                ]
                return tournaments
        except Exception as e:
            print("Failed to get tournaments:", e, flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)
