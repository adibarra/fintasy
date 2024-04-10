# @author: adibarra (Alec Ibarra)
# @description: Database class for handling transaction database operations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class TransactionsMixin:
    """
    A collection of methods for handling transaction database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_transaction(
        self, uuid_portfolio: str, symbol: str, action: str, quantity: int
    ) -> str:
        """
        Creates a new transaction in the database.

        Args:
            uuid_portfolio (str): The UUID of the portfolio.
            symbol (str): The symbol of the stock involved in the transaction.
            action (str): The action of the transaction, either 'buy' or 'sell'.
            quantity (int): The quantity of stocks involved in the transaction.

        Returns:
            str: The UUID of the created transaction if successful, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO transactions (uuid_portfolio, symbol, action, quantity) VALUES (%s, %s, %s, %s) RETURNING uuid",
                    (uuid_portfolio, symbol, action, quantity),
                )
                conn.commit()
                transaction_uuid = cursor.fetchone()[0]
                return transaction_uuid
        except Exception as e:
            print("Failed to create transaction:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_transaction(
        self, uuid_portfolio: str, offset: int = 0, limit: int = 10
    ) -> dict:
        """
        Retrieves a list of transactions for a given portfolio.

        Args:
            uuid_portfolio (str): The UUID of the portfolio.
            offset (int): The offset for paginating the results.
            limit (int): The maximum number of transactions to retrieve.

        Returns:
            dict: A dictionary containing the list of transactions if successful, None otherwise.
        """
        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM transactions WHERE uuid_portfolio = %s ORDER BY created_at DESC OFFSET %s LIMIT %s",
                    (uuid_portfolio, offset, limit),
                )
                column_names = [desc[0] for desc in cursor.description]
                transactions = [
                    dict(zip(column_names, row)) for row in cursor.fetchall()
                ]
                return transactions
        except Exception as e:
            print("Failed to retrieve transactions:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def get_transaction_by_uuid(self, uuid_transaction: str) -> dict:
        """
        Retrieves a transaction from the database by UUID.

        Args:
            uuid_transaction (str): The UUID of the transaction.

        Returns:
            dict: A dictionary representing the transaction if found, None otherwise.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM transactions WHERE uuid = %s LIMIT 1",
                    (uuid_transaction,),
                )
                column_names = [desc[0] for desc in cursor.description]
                transaction = dict(zip(column_names, cursor.fetchone()))
                return transaction
        except Exception as e:
            print("Failed to get transaction by UUID:", e, flush=True)
            return None
        finally:
            if conn:
                self.connectionPool.putconn(conn)
