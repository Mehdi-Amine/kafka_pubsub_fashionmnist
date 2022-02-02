# Fashion MNIST with Kafka and Google Pub/Sub

## Video Demo
**The following image links to a video demo:**

[![Watch the video](https://img.youtube.com/vi/TWMK9ipy6AQ/maxresdefault.jpg)](https://youtu.be/TWMK9ipy6AQ)

## Installation

1. Clone the repository with the command ```git clone https://github.com/Mehdi-Amine/kafka_pubsub_fashionmnist.git``` 
2. Alternatively, download the repository from the above green button 'code', then extract the zip file.
3. ```cd``` into the main directory with the command ```cd /path-to-be-replaced/kafka_pubsub_fashionmnist``` 
4. Create a Python virtual environment then activate it:
```
python -m venv venv
source venv/bin/activate
``` 
5. Install dependencies with the command ```pip install -r requirements.txt```

## Setup

In [Google Cloup Platform](https://console.cloud.google.com/) create a project and paste the generated project ID inside the file ```loger/setup.sh``` for the variable ```GOOGLE_CLOUD_PROJECT```. Generate a json key to authenticate and enter its path for the variable ```PUBSUB_CONFIG_PATH``` inside the file ```loger/setup.sh```. [This video](https://www.youtube.com/watch?v=xOtrCmPjal8) provides clear instructions for locating the project ID and generating the key. 

Create two Pub/Sub topics ```images``` and ```predictions```.
<img width="1280" alt="topics" src="https://user-images.githubusercontent.com/47016362/152097171-8783f7bc-59fb-4046-95d6-22e45705a9e2.png">

Then create two Pub/Sub subscribers: 
- ```images-sub```: used inside the ```loger/model_server.py``` to consume images sent by the ```loger/image_generator.py``` through the topic ``ìmages```
- ```prediction-receiver```: used inside the ```loger/result_logger.py``` to consume predictions sent by the ```loger/model_server.py```through the topic ```predictions```
<img width="1280" alt="subs" src="https://user-images.githubusercontent.com/47016362/152098711-63dfbfb4-6ca6-4e81-b010-811e690fe843.png">



## Usage
Begin by initializing a MainManager instance. Choose between 'kafka' and 'pubsub' for the backend.

```python
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
```

To use a **message consumer**, initialize a MainManager instance from ```broker/kafka_pubsub.py```, then call its function ```create_consumer()```.
```python
    def create_consumer(self, topic_id: str, callback: Callable, gcp_subscription_id:str=None):
        """create a consumer object that listen on the given topic and apply the callable function.
        
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
```

To use a **message producer**, initialize a MainManager instance from ```broker/kafka_pubsub.py```, then call its function ```create_producer()```.
```python
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
```

## References
The implementation refers to several sources:
- For the structure of the library: [AliAbdelaal/pubsub-lib](https://github.com/AliAbdelaal/pubsub-lib)
- For creating publishers and subscribers using Pub/Sub: 
  - [Publishing](https://cloud.google.com/pubsub/docs/samples/pubsub-create-push-subscription#pubsub_create_push_subscription-python)
  - [Subscribing](https://cloud.google.com/pubsub/docs/pull)
- For installing Kafka using Docker: [Better Data Science](https://www.youtube.com/watch?v=4xFZ_iTZLTs)
- For creating publishers and subscribers using Kafka: [kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html)
