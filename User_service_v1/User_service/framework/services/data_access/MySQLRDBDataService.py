import pymysql
from .BaseDataService import DataDataService  # Ensure correct import path


class MySQLRDBDataService(DataDataService):
    """
    MySQL's implementation of the DataDataService interface, supporting CRUD operations.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        """Establish a connection to the MySQL database."""
        return pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            database=self.context["database"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def fetch_one(self, table: str, key_field: str, key_value: str):
        """Fetch a single record from the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {table} WHERE {key_field} = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise
        finally:
            connection.close()

    def insert_or_update(self, table: str, data: dict, key_field: str):
        """Insert or update a record in the database."""
        connection = self._get_connection()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            updates = ", ".join([f"{key} = VALUES({key})" for key in data])

            sql = f"""
                INSERT INTO {table} ({columns}) VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {updates};
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()))
        except Exception as e:
            print(f"Error inserting or updating data: {e}")
            raise
        finally:
            connection.close()

    def delete(self, table: str, key_field: str, key_value: str):
        """Delete a record from the database."""
        connection = self._get_connection()
        try:
            sql = f"DELETE FROM {table} WHERE {key_field} = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
        except Exception as e:
            print(f"Error deleting data: {e}")
            raise
        finally:
            connection.close()

    def get_users(self, skip: int, limit: int, filters: dict):
        """Fetch users with pagination and filters."""
        query = "SELECT * FROM user_profiles WHERE 1=1"
        params = []

        if "name" in filters:
            query += " AND (first_name LIKE %s OR last_name LIKE %s)"
            params.extend([f"%{filters['name']}%"] * 2)

        if "course" in filters:
            query += " AND courses LIKE %s"
            params.append(f"%{filters['course']}%")

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, skip])

        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                # Ensure result is always a list
                return result if result else []
        finally:
            connection.close()

    def get_data_object(self, database_name: str, table_name: str, key_field: str, key_value: str):
        """Fetch a single record from the database."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table_name} WHERE {key_field} = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise
        finally:
            connection.close()