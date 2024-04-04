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

    def create_transaction(self) -> str:
        pass

    def get_transaction(self) -> str:
        pass
