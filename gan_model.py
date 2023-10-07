import torch.nn as nn

class Discriminator(nn.Module):
    def __init__(self, image_size: None):
        super(Discriminator, self).__init__()
        self.isize = image_size
        self.fc1 = nn.Linear(4 * self.isize * self.isize, 512)
        self.fc2 = nn.Linear(512, 1)
        self.activation = nn.LeakyReLU(0.1)
    def forward(self, x):
        x = x.view(-1, 4 * self.isize * self.isize)
        x = self.activation(self.fc1(x))
        x = self.fc2(x)
        return nn.Sigmoid()(x)
    
class Generator(nn.Module):
    def __init__(self, image_size: None):
        super(Generator, self).__init__()
        self.isize = image_size
        self.fc1 = nn.Linear(128, 1024)
        self.fc2 = nn.Linear(1024, 2048)
        self.fc3 = nn.Linear(2048, 4 * self.isize * self.isize)
        self.activation = nn.ReLU()
    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        x = x.view(-1, 4, self.isize, self.isize)
        return nn.Tanh()(x)