from broker_structure import GenericBroker

class GenericProducer():

    def __init__(self, backend_client:GenericBroker):
        """Create a consumer object, that listens to specific topic by the given id
        Parameters
        ----------
        backend_client : GenericBroker
            the backend object to communicate the message broker.
        """
        self.backend = backend_client

    def produce(self, value, key=None):
        """push a message on the object topic
        Parameters
        ----------
        value : bytes
            the message body
        key : str
            An optional key that can be sent with the value, by default None.
        """
        self.backend.produce(value=value, key=key)