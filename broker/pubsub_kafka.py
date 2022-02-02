import os
import json
from time import sleep
from typing import Callable
from threading import Thread
from consumer import GenericConsumer
from producer import GenericProducer
from kafka_broker import KafkaManager
from pubsub_broker import PubSubManager


class MainManager():

    def __init__(self, api: str):
        """Create a MainManager instance that you can use to initiate a consumer/producer instances.
        Parameters
        ----------
        api : str
            The backend to use, either 'kafka' or 'pubsub'
        """
        if api not in ['pubsub', 'kafka']:
            raise ValueError(f"API : `{api}` is not supported yet, only `kafka` and `google pubsup` are supported.")
        self.api = api
        self.configs = json.load(open(os.getenv('PUBSUB_CONFIG_PATH')))

    def create_consumer(self, topic_id: str, callback: Callable, gcp_subscription_id:str=None):
        """create a consumer object that listen on the given topic and apply
        the callable function.
        Parameters
        ----------
        topic_id : str
            the topic ID to listen to.
        callback : Callable
            The function to apply if a message was received.
        gcp_subscription_id : str
            The subscription ID for the PubSub topic, this is only used with GCP as backend.
        """
        backend = None
        if self.api == 'kafka':
            backend = KafkaManager(topic_id, self.configs['kafka_servers'])
            GenericConsumer(backend, callback)
        else:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            subscription_name = gcp_subscription_id
            backend = PubSubManager(project_id=project_id, topic=topic_id,
                                         subscription_name=subscription_name, pubsub_configs=self.configs, callback=callback)
            runner_thread = Thread(target=self.__thread_target)
            runner_thread.start()

    def __thread_target(self):
        while True:
            sleep(.1)

    def create_producer(self, topic_id: str):
        """create a producer object that pushes messages on the given topic.
        Parameters
        ----------
        topic_id : str
            The topic ID to push messages to.
        Returns
        -------
        GenericProducer
            The producer object.
        """
        backend = None
        if self.api == 'kafka':
            backend = KafkaManager(topic_id, self.configs['kafka_servers'])
        else:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            subscription_name = os.getenv("GOOGLE_PUBSUB_SUB_ID")
            backend = PubSubManager(project_id=project_id, topic=topic_id,
                                         subscription_name=subscription_name, pubsub_configs=self.configs)

        return GenericProducer(backend)