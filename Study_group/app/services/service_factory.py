from framework.services.service_factory import BaseServiceFactory
import app.resources.course_resource as course_resource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from dotenv import load_dotenv
import os


# TODO -- Implement this class
class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        #
        # TODO -- The terrible, hardcoding and hacking continues.
        #
        if service_name == 'StudyResource':
            result = course_resource.CourseResource(config=None)
        elif service_name == 'StudyResourceDataService':
            load_dotenv()
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            context = dict(user=db_user, password=db_password,
                           host=db_host, port=int(db_port))
            data_service = MySQLRDBDataService(context=context)
            result = data_service
        else:
            result = None

        return result
    @classmethod
    def post_service(cls, service_name):
            if service_name == 'StudyResource':
                result = course_resource.CourseResource(config=None)
            elif service_name == "StudyResourceDataService":
                load_dotenv()
                db_host = os.getenv("DB_HOST")
                db_port = os.getenv("DB_PORT")
                db_user = os.getenv("DB_USER")
                db_password = os.getenv("DB_PASSWORD")
                context = dict(user=db_user, password=db_password,
                            host=db_host, port=int(db_port))
                data_service = MySQLRDBDataService(context=context)
                return data_service
            else:
                result = None

            return result
    




