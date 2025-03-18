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

    # Additional Methods

    def get_courses_for_student(self, student_id: str):
        """Retrieve all courses a student is enrolled in."""
        connection = self._get_connection()
        try:
            sql = """
                SELECT c.course_id, c.course_code, c.course_name, c.semester, c.year
                FROM enrollments e
                JOIN courses c ON e.course_code = c.course_code
                WHERE e.student_id = %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, (student_id,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error fetching courses for student: {e}")
            raise
        finally:
            connection.close()

    def get_students_in_course(self, course_code: str):
        """Retrieve all students enrolled in a specific course."""
        connection = self._get_connection()
        try:
            sql = """
                SELECT s.student_id, s.first_name, s.last_name, s.email, s.university_id
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                WHERE e.course_code = %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, (course_code,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error fetching students for course: {e}")
            raise
        finally:
            connection.close()

    def course_exists(self, course_code: str):
        """Check if a course exists in the database by its course_code."""
        connection = self._get_connection()
        try:
            sql = "SELECT 1 FROM courses WHERE course_code = %s LIMIT 1"
            with connection.cursor() as cursor:
                cursor.execute(sql, (course_code,))
                result = cursor.fetchone()
                return result is not None  # Returns True if course exists, False otherwise
        except Exception as e:
            print(f"Error checking if course exists: {e}")
            raise
        finally:
            connection.close()
