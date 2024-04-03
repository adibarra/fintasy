# @author: adibarra (Alec Ibarra)
# @description: Database class mixin for handling meta database operations

from typing import Any, Dict, List


class MetaMixin:
    """
    A collection of methods for handling meta database operations.
    """

    def query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        !!! DO NOT USE THIS IN PRODUCTION CODE !!!\n
        Executes a query on the database.

        Args:
            query (str): The query to execute.
            params (tuple): The parameters to pass to the query.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the results of the query.
        """

        conn = None
        result = []

        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    column_names = [desc[0] for desc in cursor.description]
                    for row in cursor.fetchall():
                        result.append(
                            dict(zip(column_names, [str(value) for value in row]))
                        )
                conn.commit()
                return result
        except Exception as e:
            print(f"Failed to execute query: ({query[:20]}) {e}")
        finally:
            if conn:
                self.connectionPool.putconn(conn)

    def show_tables(self) -> List[str]:
        """
        !!! DO NOT USE THIS IN PRODUCTION CODE !!!\n
        Retrieves a list of table names from the database.

        Returns:
            A list of table names as strings.
        """

        conn = None
        try:
            conn = self.connectionPool.getconn()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
                )
                result = cursor.fetchall()
                conn.commit()
                return [table[0] for table in result]
        except Exception as e:
            print("Failed to show tables:", e)
            return []
        finally:
            if conn:
                self.connectionPool.putconn(conn)
