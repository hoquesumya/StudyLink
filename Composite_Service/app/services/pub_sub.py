import threading
from app.services.service_factory import ServiceFactory
class Publisher:
    def __init__(self):
        self.subscribers = {}
 
    def subscribe(self, subscriber, topic):
        print(topic, subscriber)
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)
 
    def publish(self, message, topic, params):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.event.set()
                subscriber.message = message
                subscriber.params = params
 
class Subscriber:
    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        self.message = None
        self.params = []
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
        self.user_error = False
 
    def receive(self):
        self.event.wait()
        #will sent the request to the client
        print(f"{self.name}" +"received message:" + f"{self.message}")
        if self.message == "Get User":
            response_data_get, status_code = self.compo_resource.get_user(self.params[0],self.params[1], self.params[2])
            if  status_code != 200:
               self.event.clear()
               self.user_error = True
               return (False, response_data_get, status_code)
            else:
               self.event.clear()
               return (True, response_data_get, status_code)
        if self.message == "Get chat":
            print("messge", self.params[0])
            response_post, status_code = self.compo_resource.post_chat(self.params[0])
            if status_code != 200:
                self.event.clear()
                return (False, response_post, status_code)
            else:
                 return (True, response_post, status_code)
            




        #print(f"{self.name}" +"received message:" + {self.message})
        #self.event.clear()
 
 