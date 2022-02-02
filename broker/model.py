import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 14, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(14, 7, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(7 * 7 * 7, 28) 
        self.fc2 = nn.Linear(28, 10)

    def forward(self, x):
        out = F.max_pool2d(F.relu(self.conv1(x)), 2)
        out = F.max_pool2d(F.relu(self.conv2(out)), 2)
        out = torch.flatten(out, 1)
        out = F.relu(self.fc1(out))
        out = self.fc2(out)
        return out
