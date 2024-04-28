# @author: adibarra (Alec Ibarra)
# @description: Database class for handling portfolio database operations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class PortfolioMixin:
    """
    A collection of methods for handling portfolio database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_portfolio(
        self, uuid_user: str, name: str, tournament_uuid: str = None
    ) -> dict:
        """
        Creates a new portfolio in the database.

        Args:
            uuid_user (str): The UUID of the user associated with the portfolio.
            name (str): The name of the portfolio.
            tournament (str, optional): The UUID of the tournament associated with the portfolio.

        Returns:
            dict: A dictionary representing the created portfolio if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO portfolios (owner, name, tournament) VALUES (%s, %s, %s) RETURNING *",
                    (uuid_user, name, tournament_uuid),
                )
                portfolio = cursor.fetchone()
                conn.commit()
                if portfolio is not None:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, portfolio))
                else:
                    print("Failed to retrieve the created portfolio.", flush=True)
                    return None
        except Exception as e:
            print("Failed to create portfolio:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_portfolio(self, uuid_portfolio: str) -> dict:
        """
        Retrieves a portfolio from the database by UUID.

        Args:
            uuid_portfolio (str): The UUID of the portfolio.

        Returns:
            dict: A dictionary representing the portfolio if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM portfolios WHERE uuid = %s LIMIT 1",
                    (uuid_portfolio,),
                )
                if cursor.description:
                    portfolio = cursor.fetchone()
                    if portfolio is not None:
                        column_names = [desc[0] for desc in cursor.description]
                        return dict(zip(column_names, portfolio))
                    else:
                        print(
                            f"Portfolio with UUID '{uuid_portfolio}' not found.",
                            flush=True,
                        )
                        return None
        except Exception as e:
            print("Failed to get portfolio by UUID:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_portfolios(
        self,
        owner: str = None,
        tournament: str = None,
        name: str = None,
        offset: int = None,
        limit: int = None,
    ):
        """
        Retrieves a list of portfolios from the database.

        Args:
            owner (str, optional): The UUID of the user associated with the portfolios.
            tournament (str, optional): The UUID of the tournament associated with the portfolios.
            name (str, optional): The name of the portfolios.
            offset (int, optional): The number of portfolios to skip.
            limit (int, optional): The maximum number of portfolios to retrieve.

        Returns:
            list: A list of dictionaries representing the portfolios if found, an empty list otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                params = []
                query = "SELECT * FROM portfolios WHERE TRUE"
                if owner is not None:
                    query += " AND owner = %s"
                    params.append(str(owner))
                if tournament is not None:
                    query += " AND tournament = %s"
                    params.append(str(tournament))
                if name is not None:
                    query += " AND name = %s"
                    params.append(name)
                if offset is None:
                    offset = 0
                if limit is None:
                    limit = 10
                query += f" OFFSET {offset} LIMIT {limit}"
                cursor.execute(query, params)
                if cursor.description:
                    portfolios = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]
                    return [
                        dict(zip(column_names, portfolio)) for portfolio in portfolios
                    ]
                else:
                    print("No portfolios found.", flush=True)
                    return []
        except Exception as e:
            print("Failed to get portfolios:", e, flush=True)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_portfolio(self, uuid_portfolio: str, name: str) -> bool:
        """
        Updates the name of a portfolio in the database by UUID.

        Args:
            uuid_portfolio (str): The UUID of the portfolio to update.
            name (str): The new name for the portfolio.

        Returns:
            bool: True if the portfolio was successfully updated, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE portfolios SET name = %s WHERE uuid = %s",
                    (name, uuid_portfolio),
                )
                conn.commit()
                return True
        except Exception as e:
            print("Failed to update portfolio by UUID:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def update_portfolio_balance(self, uuid_portfolio: str, balance_cents: int) -> bool:
        """
        Updates the name of a portfolio in the database by UUID.

        Args:
            uuid_portfolio (str): The UUID of the portfolio to update.
            balance_cents (int): The new balance for the portfolio.

        Returns:
            bool: True if the portfolio was successfully updated, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE portfolios SET balance_cents = %s WHERE uuid = %s",
                    (balance_cents, uuid_portfolio),
                )
                conn.commit()
                return True
        except Exception as e:
            print("Failed to update portfolio balance by UUID:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def delete_portfolio(self, uuid_portfolio: str) -> bool:
        """
        Deletes a portfolio from the database by UUID.

        Args:
            uuid_portfolio (str): The UUID of the portfolio to delete.

        Returns:
            bool: True if the portfolio was successfully deleted, False otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM portfolios WHERE uuid = %s", (uuid_portfolio,)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Failed to delete portfolio by UUID:", e, flush=True)
            return False
        finally:
            if conn:
                self.connectionPool.putconn(conn)
