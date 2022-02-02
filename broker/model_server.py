import io
import json
import torch

from model import Net
from pubsub_kafka import MainManager

BACKEND = 'pubsub'
FROM_TOPIC_ID = 'images'
# specific to google pubsub
FROM_SUBSCRIPTION_ID = 'images-sub'
TO_TOPIC_ID = 'predictions'
global model, producer


def predict_img(key, value):
    global model, producer
    img = torch.load(io.BytesIO(value))
    predictions = model(img.unsqueeze(0))
    pred_index = torch.max(predictions, 1)[1].item()
    pred_label = output_label(pred_index)
    predictions = f"predicted label: {pred_index}, predicted name: {pred_label}"
    producer.produce(json.dumps(predictions).encode(), key=key)
    print(f'got an image with shape {img.shape}, classified and pushed.')
    print()

def output_label(label):
    output_mapping = {
                 0: "T-shirt/Top",
                 1: "Trouser",
                 2: "Pullover",
                 3: "Dress",
                 4: "Coat", 
                 5: "Sandal", 
                 6: "Shirt",
                 7: "Sneaker",
                 8: "Bag",
                 9: "Ankle Boot"
                 }
    input = (label.item() if type(label) == torch.Tensor else label)
    return output_mapping[input]

model = Net()
model_path = 'broker/model/checkpoint.pth'
model.load_state_dict(torch.load(model_path))

pubsub = MainManager(BACKEND)

# create a producer to publish predictions
producer = pubsub.create_producer(TO_TOPIC_ID)

# create a consumer to load images
consumer = pubsub.create_consumer(FROM_TOPIC_ID, predict_img, FROM_SUBSCRIPTION_ID)
print("classifier consumer service started...")
print("classifier producer service started...")