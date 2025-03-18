import pymysql
from .BaseDataService import DataDataService
import logging

# Configure logger for this module
logger = logging.getLogger("MySQLRDBDataService")
logger.setLevel(logging.INFO)  # Set to INFO for less verbose logs in production


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implements common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods, and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        """Establish and return a MySQL connection."""
        try:
            logger.info("Connecting to the database...")
            connection = pymysql.connect(
                host=self.context["host"],
                port=self.context["port"],
                user=self.context["user"],
                passwd=self.context["password"],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            logger.info("Database connection established.")
            return connection
        except Exception as e:
            logger.exception("Failed to connect to the database.")
            raise

    def get_data_object(self, database_name: str, collection_name: str, key_field: str, key_value: str):
        """Retrieve a single data object based on key_field and key_value."""
        connection = None
        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} WHERE {key_field}=%s"
            logger.debug("Executing query to fetch a data object.")
            connection = self._get_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql_statement, [key_value])
                result = cursor.fetchone()
                if result:
                    logger.info("Successfully retrieved a data object.")
                else:
                    logger.info(f"No data object found for {key_field} = {key_value}.")
                return result
        except Exception as e:
            logger.exception("Error retrieving data object.")
            raise
        finally:
            if connection:
                connection.close()
                logger.debug("Database connection closed.")

    def fetch_one(self, database_name: str, table: str, key_field: str, key_value: str):
        """Fetch a single record from the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table} WHERE {key_field} = %s"
            logger.debug("Executing query to fetch a single record.")
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
                result = cursor.fetchone()
                if result:
                    logger.info(f"Successfully fetched a record from {table}.")
                else:
                    logger.info(f"No record found in {table} where {key_field} = {key_value}.")
                return result
        except Exception as e:
            logger.exception("Error fetching a single record.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def insert(self, database_name: str, table: str, data: dict):
        """Insert a new record into the database."""
        connection = self._get_connection()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            sql = f"INSERT INTO {database_name}.{table} ({columns}) VALUES ({placeholders})"
            logger.debug("Executing query to insert a record.")
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()))
                inserted_id = cursor.lastrowid
                logger.info(f"Record inserted into {table} with ID {inserted_id}.")
                return inserted_id
        except Exception as e:
            logger.exception("Error inserting record.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def fetch_all(self, database_name: str, table: str):
        """Fetch all records from the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table}"
            logger.debug("Executing query to fetch all records.")
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.info(f"Fetched {len(result)} records from {table}.")
                return result
        except Exception as e:
            logger.exception("Error fetching all records.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def fetch_paginated(self, database_name: str, table: str, offset: int, limit: int):
        """Fetch a paginated list of records from the table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table} LIMIT %s OFFSET %s"
            logger.debug("Executing query to fetch paginated records.")
            with connection.cursor() as cursor:
                cursor.execute(sql, (limit, offset))
                result = cursor.fetchall()
                logger.info(f"Fetched {len(result)} records from {table} (offset: {offset}, limit: {limit}).")
                return result
        except Exception as e:
            logger.exception("Error fetching paginated data.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def update(self, database_name: str, table: str, data: dict, key_field: str, key_value: str):
        """Update an existing record in the database."""
        connection = self._get_connection()
        try:
            existing_record = self.fetch_one(database_name, table, key_field, key_value)
            if not existing_record:
                logger.warning(f"No record found in {table} for update where {key_field} = {key_value}.")
                raise Exception(f"No record found with {key_field} = {key_value}")
            
            updates = ", ".join([f"{key} = %s" for key in data.keys()])
            sql = f"UPDATE {database_name}.{table} SET {updates} WHERE {key_field} = %s"
            logger.debug("Executing query to update a record.")
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()) + (key_value,))
                logger.info(f"Record in {table} updated where {key_field} = {key_value}.")
        except Exception as e:
            logger.exception("Error updating record.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def delete(self, database_name: str, table: str, key_field: str, key_value: str):
        """Delete a record from the specified table asynchronously."""
        connection = self._get_connection()
        try:
            # Check if the record exists
            existing_record = self.fetch_one(database_name, table, key_field, key_value)
            if not existing_record:
                logger.warning(f"No record found in {table} for deletion where {key_field} = {key_value}.")
                raise Exception(f"No record found with {key_field} = {key_value}")
            
            # Delete the record
            sql = f"DELETE FROM {database_name}.{table} WHERE {key_field} = %s"
            logger.debug("Executing query to delete a record.")
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
                logger.info(f"Record deleted from {table} where {key_field} = {key_value}.")

        except Exception as e:
            logger.exception("Error deleting record.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")

    def count_all(self, database_name: str, table: str) -> int:
        """Count all records in the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT COUNT(*) AS total FROM {database_name}.{table}"
            logger.debug("Executing query to count records.")
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                logger.info(f"Table {table} contains {result['total']} records.")
                return result['total']
        except Exception as e:
            logger.exception("Error counting records.")
            raise
        finally:
            connection.close()
            logger.debug("Database connection closed.")