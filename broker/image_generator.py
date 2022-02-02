import io
import torch
import torchvision
from torchvision import transforms

from pubsub_kafka import MainManager

BACKEND = 'pubsub'
TOPIC_ID = 'images'

# loading data 
test_set = torchvision.datasets.FashionMNIST(
    "./data", download=True, train=False, transform=transforms.Compose([transforms.ToTensor()]))

# create a producer object
pubsub = MainManager(BACKEND)
producer = pubsub.create_producer(TOPIC_ID)
print("Image generator started...")

# start pushing images to the topic
for i, img in enumerate(test_set):
    img, label = img[0], img[1]
    # transform image tensor to bytes string
    with io.BytesIO() as buff:
        buff = io.BytesIO()
        torch.save(img, buff)
        buff.seek(0)
        key = f'img-{i}-label-{label}'
        producer.produce(buff.getvalue(), key=key.encode())
        print(f'pushed image labeled: {test_set.classes[label]}.')
    prompt = input("Continue ? ")
    if prompt =='n':
        break