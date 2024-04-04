# @author: adibarra (Alec Ibarra)
# @description: Database class for handling tournament database operations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg2.pool import SimpleConnectionPool


class TournamentsMixin:
    """
    A collection of methods for handling tournament database operations.
    """

    connectionPool: "SimpleConnectionPool"

    def create_tournament(self) -> str:
        pass

    def get_tournament(self) -> str:
        pass

    def update_tournament(self) -> str:
        pass

    def delete_tournament(self) -> str:
        pass
