from framework.services.service_factory import BaseServiceFactory
import app.resources.course_resource as course_resource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService


class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'CourseResource':
            result = course_resource.CourseResource(config=None)
        elif service_name == 'CourseResourceDataService':
            context = dict(
                user="root",
                password="dbuserdbuser",
                host="localhost",
                port=3306,
                database= "CloudComputing_CE"
            )
            result = MySQLRDBDataService(context=context)
        elif service_name == 'CourseEnrollmentService':
            context = dict(
                user="root",
                password="dbuserdbuser",
                host="localhost",
                port=3306
            )
            result = CourseEnrollmentService(context=context)
        else:
            raise ValueError(f"Service {service_name} is not supported.")

        return result
