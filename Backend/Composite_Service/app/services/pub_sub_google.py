from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from dotenv import load_dotenv
import os, json
class Publisher:
    def __init__(self) -> None:
        load_dotenv()
        self.project_id = os.getenv("PROJECT")
        self.topic_id = os.getenv("TOPIC_PUB_SUB")
    def publish_message(self, element_http : dict):
        publisher = pubsub_v1.PublisherClient()
        # The `topic_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/topics/{topic_id}`
        topic_path = publisher.topic_path(self.project_id, self.topic_id)
        print(topic_path)
        json_string = json.dumps(element_http)
        data = json_string.encode("utf-8")
        print(data)
        future = publisher.publish(topic_path, data)
        print(future.result())  
class Subscriber:
    def __init__(self) -> None:
        load_dotenv()
        self.project_id = os.getenv("PROJECT")
        self.subs_id = os.getenv("SUBSCRIPTION_ID")
        self.subscriber = pubsub_v1.SubscriberClient()
        self.timeout = 20
        self.response_object = None
        self.status = 200
        
    
    def subscribe(self):
        
        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            print(f"Received {message}.")
            message_data = message.data.decode('utf-8')
            json_data = json.loads(message_data)
            self.response_object = json_data["response"]
            self.status = json_data["status"]
        # Access fields in the JSON object
            print(f"Received JSON message: {json_data}")
            message.ack()
        subscription_path = self.subscriber.subscription_path(self.project_id, self.subs_id)

        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}..\n")

        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with self.subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=self.timeout)
            except TimeoutError:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.
    def get_response(self):
        return (self.response_object, self.status)
        

