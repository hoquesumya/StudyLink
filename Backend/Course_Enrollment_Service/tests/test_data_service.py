from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService

# Define the database context
context = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "dbuserdbuser",  # Replace with your actual password
    "database": "CloudComputing_CE"
}

# Initialize the data service
data_service = MySQLRDBDataService(context)

# Test the connection by fetching all students (or another sample query)
try:
    connection = data_service._get_connection()
    print("Database connection successful!")
    # Test a query (fetch all students)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students;")
        result = cursor.fetchall()
        print("Fetched students:", result)
finally:
    connection.close()
