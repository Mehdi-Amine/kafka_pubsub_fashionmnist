import json
from pubsub_kafka import MainManager 

BACKEND = 'pubsub'
FROM_TOPIC_ID = 'predictions'
FROM_SUBSCRIPTION_ID = 'prediction-receiver'


def callback(key, value):
    value = json.loads(value.decode())
    print(f"Log result received:\n{json.dumps(value, indent=2)}\n\n")

# create a consumer
pubsub = MainManager(BACKEND)
consumer = pubsub.create_consumer(FROM_TOPIC_ID, callback, FROM_SUBSCRIPTION_ID)
print("Logger service started...")