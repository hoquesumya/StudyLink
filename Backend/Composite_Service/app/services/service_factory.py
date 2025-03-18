from framework.services.service_factory import BaseServiceFactory

from framework.data_access.Composite_config import CompositeConfig
from dotenv import load_dotenv

import os
class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == "CompositeResourceService":
            load_dotenv()
            user_microservice = os.getenv("USER_MICRO")
            study_microservice = os.getenv("STUDY_MICRO")
            chat_microservice = os.getenv("CHAT_MICRO")
            course_service = os.getenv("COURSE_MICRO")
            return CompositeConfig(user_microservice, chat_microservice, study_microservice, course_service)
        if service_name == "CompositeResource":
            from app.resources.composite_resource import CompositeResource
            return CompositeResource()
        else:
            raise ValueError(f"Service {service_name} is not accepteable")

    