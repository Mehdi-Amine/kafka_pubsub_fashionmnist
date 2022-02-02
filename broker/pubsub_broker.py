import os
import json
from typing import Callable, Tuple
from google.auth import jwt
from google.cloud import pubsub_v1

from broker_structure import GenericBroker

# JWT audience
P_AUDIENCE = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
S_AUDIENCE = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

class PubSubManager(GenericBroker):
    """Class used to aggregate the publisher and subscriber functions for Google Pub/Sub.

    Attributes
    ----------
    topic_path : str
        Composed from the topic and project_id to construct the path 'projects/{project_id}/topics/{topic}' 
    subscription_path : str
        Composed from the subscription_name and project_id to construct the path 'projects/{project_id}/subscriptions/{subscription_id}'
    producer : pubsub_v1.PublisherClient()
        instance from the class PublisherClient()
    consumer : pubsub_v1.SubscriberClient()
        instance from the class SubscriberClient()

    Methods
    -------
    produce(value, key)
        Takes the value and key of the message to publish on the topic.
    consume()
        Pulls messages from the topic.
    __acknowledge(callback)
        method wrapper for the callback attribute. Used to acknowledge receipt of messages.
    """

    def __init__(self, topic, project_id, subscription_name, pubsub_configs, callback:Callable=None) -> None:
        """Initiate a Google Pub/Sub client.
        Parameters
        ----------
        topic : str
            The topic name used to construct the topic path.
        project_id : str
            The project ID used to construct the topic and subscription paths.
        subscription_name : str
            The subscription name used to construct the subscription path.
        pubsub_configs : dict
            credentials and settings extracted from the key json file provided from GCP Pub/Sub.
        callback : Callable
            Callable attribute defining the method to execute after pulling a message.
        """
        
        # JWT reference https://google-auth.readthedocs.io/en/master/reference/google.auth.jwt.html
        subscriber_credentials = jwt.Credentials.from_service_account_info(pubsub_configs, audience=S_AUDIENCE)
        publisher_credentials = subscriber_credentials.with_claims(audience=P_AUDIENCE)
        self.topic_path = f'projects/{project_id}/topics/{topic}'
        self.subscription_path = f'projects/{project_id}/subscriptions/{subscription_name}'
        self.consumer = pubsub_v1.SubscriberClient(credentials=subscriber_credentials)
        publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        self.producer = pubsub_v1.PublisherClient(credentials=publisher_credentials, publisher_options=publisher_options)
        
        if callback:
            self.consumer.subscribe(self.subscription_path, self.__acknowledge(callback))
    
    def __acknowledge(self, callback):
        def wrappedCallback(message):
            callback(message.attributes.get('key', None), message.data)
            message.ack()
        return wrappedCallback


    def produce(self, value, key=None):
        """Method for pushing messages with a PubSub publisher.

        Parameters
        ----------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        self.producer.publish(self.topic_path, value, key)

    def consume(self) -> Tuple[str, bytes]:
        """Method for pulling messages with a PubSub subscriber.
        
        Returns
        -------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        raise NotImplementedError()