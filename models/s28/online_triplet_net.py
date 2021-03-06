import torch.nn as nn
import torch.nn.functional as F

from config import get_config
from datasets.ordered_sampler import select_triplets


class OnlineTripletNet(nn.Module):
    def __init__(self, channel=1, embedding_size=10, **kwargs):
        super(OnlineTripletNet, self).__init__()
        config = get_config()
        self.conv1 = nn.Conv2d(channel, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, embedding_size)
        self.label_count = config.label_count

    def forward_once(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        x = F.normalize(x, p=2, dim=1)
        return x

    def forward(self, x):
        x = self.forward_once(x)
        x = F.log_softmax(x)
        return select_triplets(x, 256 / self.label_count, self.label_count, 1)


def get_network():
    return OnlineTripletNet


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--trainer', type=str, default="listwise")
    parser.add_argument('--width', type=int, default=28)
    parser.add_argument('--height', type=int, default=28)
    parser.add_argument('--channel', type=int, default=3)
    parser.add_argument('--data_name', type=str, default="mnist")
    parser.add_argument('--loader_name', type=str, default="data_loaders")
    parser.add_argument('--label_count', type=int, default=8)
    import torch
    from config import set_config, get_config

    args = parser.parse_args()

    kwargs = vars(args)
    trainer_name = kwargs['trainer']
    kwargs.pop('trainer')

    set_config(trainer_name, **kwargs)
    import torch
    from torch.autograd import Variable

    N = 256
    input_dim = 28
    output_dim = 10
    channel = 3
    model = get_network()(channel=channel, embedding_size=output_dim)

    x = Variable(torch.randn(N, channel, input_dim, input_dim))
    y = Variable(torch.randn(N, output_dim), requires_grad=False)

    criterion = torch.nn.MSELoss(size_average=False)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
    for t in range(5):
        y_pred = model(x)

        loss = criterion(y_pred, y)
        print(t, loss.data[0])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
