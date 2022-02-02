from typing import Callable
from threading import Thread
from time import sleep

from broker_structure import GenericBroker

class GenericConsumer():

    def __init__(self, backend_client:GenericBroker, callback:Callable):
        """Create a consumer object, that listens to specific topic by the given id
        Parameters
        ----------
        backend_client : GenericBroker
            the backend object to communicate the message broker.
        callback : Callable
            the callback function to call when a new message comes along
            the function must accept two kwargs: key and value.
        """
        self.backend = backend_client
        self.callback = callback
        listener_thread = Thread(target=self.__consume())
        listener_thread.start()

    def __consume(self):
        """listen to the topic and invoke the callback on each new msg.
        """
        while True:
            sleep(.1)
            key, value = self.backend.consume()
            self.callback(key=key, value=value)