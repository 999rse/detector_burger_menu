import os
import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.transforms import transforms


from c_dataloader import BurgerMenu_Dataset
from gan_model import Discriminator, Generator


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

isize = 120
epochs = 100
lr = 2e-4
batch_size = 32
loss = nn.BCELoss()

# Model
G = Generator(image_size=isize).to(device)
D = Discriminator(image_size=isize).to(device)

G_optimizer = optim.Adam(G.parameters(), lr=lr)
D_optimizer = optim.Adam(D.parameters(), lr=lr)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485], std=[0.229]),
    transforms.Resize([isize,isize])
    ])


# Load custom dataset
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

data = 'dataset'
dataset = BurgerMenu_Dataset(data, transform=transform)
train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)



def GAN(train_loader, epochs, G_optimizer, D_optimizer, loss, device):
    if not os.path.exists('./models/gan'):
        os.makedirs('./models/gan')

    for epoch in range(epochs):
        for idx, (imgs, _) in enumerate(train_loader):
            idx += 1
            real_inputs = imgs.to(device)
            real_outputs = D(real_inputs)
            real_label = torch.ones(real_inputs.shape[0], 1).to(device)

            noise = (torch.rand(real_inputs.shape[0], 128) - 0.5) / 0.5
            noise = noise.to(device)
            fake_inputs = G(noise)
            fake_outputs = D(fake_inputs)
            fake_label = torch.zeros(fake_inputs.shape[0], 1).to(device)
            outputs = torch.cat((real_outputs, fake_outputs), 0)
            targets = torch.cat((real_label, fake_label), 0)

            D_loss = loss(outputs, targets)
            D_optimizer.zero_grad()
            D_loss.backward()
            D_optimizer.step()

            noise = (torch.rand(real_inputs.shape[0], 128)-0.5)/0.5
            noise = noise.to(device)
            fake_inputs = G(noise)
            fake_outputs = D(fake_inputs)
            fake_targets = torch.ones([fake_inputs.shape[0], 1]).to(device)

            G_loss = loss(fake_outputs, fake_targets)
            G_optimizer.zero_grad()
            G_loss.backward()
            G_optimizer.step()

            if idx % 100 == 0 or idx == len(train_loader):
                print('Epoch {} Iteration {}: discriminator_loss {:.3f} generator_loss {:.3f}'.format(epoch, idx, D_loss.item(), G_loss.item()))
        if (epoch+1) % 10 == 0:
            torch.save(G, './models/gan/Generator_epoch_{}.pth'.format(epoch))
            print('Model saved.')


GAN(train_loader, epochs, G_optimizer, D_optimizer, loss, device)