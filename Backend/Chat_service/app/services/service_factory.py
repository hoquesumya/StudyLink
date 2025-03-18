from framework.services.service_factory import BaseServiceFactory
from app.resources.conversation_resource import ConversationResource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from dotenv import load_dotenv
import os
import logging

# Configure logging
logger = logging.getLogger("ServiceFactory")
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs; adjust as needed

class ServiceFactory(BaseServiceFactory):
    def __init__(self):
        super().__init__()

    # Load environment variables from .env file
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        logger.warning(f".env file not found at {env_path}")

    @classmethod
    def get_service(cls, service_name):
        """
        Retrieve a service instance based on the provided service name.
        
        :param service_name: The name of the service to instantiate.
        :return: An instance of the requested service.
        :raises ValueError: If the service name is not supported.
        """
        logger.info(f"Attempting to retrieve service: {service_name}")

        try:
            if service_name == 'ConversationResourceService':
                # Prepare database connection context
                context = {
                    "host": os.getenv("DB_HOST"),
                    "port": int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not defined
                    "user": os.getenv("DB_USER"),
                    "password": os.getenv("DB_PASSWORD"),
                    "database": os.getenv("DB_NAME")
                }
                # Mask sensitive data in logs
                masked_context = {**context, "password": "******"}
                logger.debug(f"Database connection context: {masked_context}")

                service = MySQLRDBDataService(context)
                logger.info(f"Successfully instantiated service: {service_name}")
                return service

            elif service_name == 'ConversationResource':
                service = ConversationResource()
                return service

            else:
                logger.error(f"Service {service_name} is not supported.")
                raise ValueError(f"Service {service_name} is not supported.")

        except Exception as e:
            logger.exception(f"Error occurred while retrieving service: {service_name}")
            raise