import json
import logging
from typing import Dict, Any, List

import pymysql
from .BaseDataService import DataDataService


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        logging.debug("Establishing MySQL database connection.")
        connection = pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        logging.debug("Connection established.")
        return connection

    def get_all_objects(self,
                database_name: str,
                collection_name: str):
        connection = None
        try:
            logging.info(f"Fetching all objects from {database_name}.{collection_name}")
            sql_statement = f"SELECT * FROM {database_name}.{collection_name}"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement)

            # Fetch all results from the executed query
            results = cursor.fetchall()
            logging.info(f"Fetched {len(results)} records.")

            return results  # Return all records as a list of dictionaries
        except Exception as e:
            print(f"Error in get_all: {e}")
            return []  # Return an empty list in case of failure
        finally:
            if connection:
                connection.close()
                logging.debug("MySQL connection closed.")

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} "+ \
                        f"where {key_field}=%s"
            logging.debug(f"Executing query: {sql_statement} with key_value: {key_value}")
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
            logging.info(f"Fetched data for {key_field}={key_value}: {result}")
        except Exception as e:
            logging.error(f"Error in get_data_object: {e}")
        finally:
            if connection:
                connection.close()
                logging.debug("MySQL connection closed.")

        return result


    def post_data_object(self,
                         database_name: str,
                         collection_name: str,
                         group_name: str,
                         created_at: str,
                         created_by: str,
                         course_id: int,
                         is_recurring: bool,
                         meeting_date: str,
                         recurrence_frequency: str,
                         recurrence_end_date: str,
                         start_time: str,
                         end_time: str,
                         members: List[str]):
        connection = None
        try:
            if created_by not in members:
                members.append(created_by)
            members_json = json.dumps(members)

            sql_statement = f"""
            INSERT INTO {database_name}.{collection_name} 
            (group_name, created_by, created_at, is_recurring, meeting_date, 
             recurrence_frequency, start_time, end_time, recurrence_end_date, course_id, members)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Get the database connection
            logging.debug(f"Executing query to insert study group: {sql_statement}")
            connection = self._get_connection()
            cursor = connection.cursor()

    # Fetch all results from the executed query

            # Execute the query
            cursor.execute(sql_statement, (group_name, created_by, created_at, is_recurring, meeting_date, recurrence_frequency,
                                           start_time, end_time, recurrence_end_date, course_id, members_json))

            connection.commit()  # Commit the transaction
            group_id = cursor.lastrowid
            logging.info(f"Study group created with ID: {group_id}")

            # Fetch all records from the table for verification
            cursor.execute(f"SELECT * FROM {database_name}.{collection_name}")
            results = cursor.fetchall()
            logging.info('Inserted record successfully. Current table data:')
            print(results)
            for row in results:
                logging.info(row)
            return group_id

        except Exception as e:
            logging.error(f"Error creating group: {e}")
        finally:
            if connection:
                connection.close()
                logging.debug("MySQL connection closed.")

    def delete_data_object(self, database_name: str, collection_name: str, key_field: str, key_value: int) -> bool:
        connection = None
        try:
            sql_statement = f"DELETE FROM {database_name}.{collection_name} WHERE {key_field}=%s"
            logging.debug(f"Executing delete query: {sql_statement} with key_value: {key_value}")
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            connection.commit()
            success = cursor.rowcount > 0  # Return True if rows were affected
            logging.info(f"Delete operation successful: {success}")
            return success
        except Exception as e:
            logging.error(f"Error in delete_data_object: {e}")
            return False
        finally:
            if connection:
                connection.close()
                logging.debug("MySQL connection closed.")

    def update_data_object(self, database_name: str, collection_name: str, key_field: str, key_value: int,
                           update_data: Dict[str, Any]) -> bool:
        connection = None
        try:
            # Convert 'members' to JSON string if it exists in update_data
            if 'members' in update_data and isinstance(update_data['members'], list):
                update_data['members'] = json.dumps(update_data['members'])

            set_clause = ", ".join([f"{field}=%s" for field in update_data.keys()])
            print('set_clause:', set_clause)
            sql_statement = f"UPDATE {database_name}.{collection_name} SET {set_clause} WHERE {key_field}=%s"

            logging.debug(f"Executing update query: {sql_statement} with key_value: {key_value} and update_data: {update_data}")
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(update_data.values()) + [key_value])
            connection.commit()
            success = cursor.rowcount > 0  # Return True if rows were affected
            logging.info(f"Update operation successful: {success}")
            return success
        except Exception as e:
            logging.error(f"Error in update_data_object: {e}")
            return False
        finally:
            if connection:
                connection.close()
                logging.debug("MySQL connection closed.")
