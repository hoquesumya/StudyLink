from abc import ABC, abstractmethod, abstractclassmethod
from typing import Any


class BaseResource(ABC):

    def __init__(self, config):
        self.config = config
    
    @classmethod
    @abstractmethod
    def get_service(cls, service_name):
        raise NotImplementedError()