from typing import Tuple

class GenericBroker():
    """Class used to unify the publish and consume functions for message brokers.

    Attributes
    ----------
    topic : str
        the topic reference for pushing and pulling messages.

    Methods
    -------
    produce(value, key)
        Takes the value and key of the message to publish on the topic.
    consume()
        Pulls messages from the topic.
    """
    def __init__(self, topic, *args, **kwargs) -> None:
        self.topic = topic
        raise NotImplementedError()

    def produce(self, value, key=None):
        """Abstract method to override with the appropriate pushing protocol required by the selected backend.

        Parameters
        ----------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        raise NotImplementedError()

    def consume(self) -> Tuple[str, bytes]:
        """Abstract method to override with the appropriate pulling protocol required by the selected backend.
        
        Returns
        -------
        value : bytes
            The content of the message.
        key : str
            The key of the message.    
        """
        raise NotImplementedError()