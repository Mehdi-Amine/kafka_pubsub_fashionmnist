from typing import Tuple
from kafka import KafkaConsumer, KafkaProducer

from broker_structure import GenericBroker


class KafkaManager(GenericBroker):
    """Class used to aggregate the producer and consumer functions for Kafka.

    Attributes
    ----------
    topic : str
        the topic reference for pushing and pulling messages.
    producer : KafkaProducer
        instance from the class KafkaProducer()
    consumer : KafkaConsumer

    Methods
    -------
    produce(value, key)
        Takes the value and key of the message to publish on the topic.
    consume()
        Pulls messages from the topic.
    """

    def __init__(self, topic, bootstrap_servers) -> None:
        """Initiate a Kafka client.
        Parameters
        ----------
        topic : str
            The topic to pub/sub with.
        bootstrap_servers : str or list of str
            Kafka server uri.
        """
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
                                      auto_offset_reset='earliest', enable_auto_commit=True,
                                      group_id='consumers')


    def produce(self, value, key=None):
        """Method for pushing messages with a Kafka producer.

        Parameters
        ----------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        self.producer.send(self.topic, key=key, value=value)
        self.producer.flush()

    def consume(self) -> Tuple[str, bytes]:
        """Method for pulling messages with a Kafka consumer.
        
        Returns
        -------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        for message in self.consumer:
            if message.key:
                key = message.key.decode()
            else:
                key = None
            return key, message.value