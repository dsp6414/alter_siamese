import torch

from models.s224.dense.net import DenseNet


class TripDenseNet(DenseNet):
    def forward(self, (input1, input2, input3)):
        x = torch.cat([input1, input2, input3], dim=1)
        output = self.forward_once(x)
        output = output.view(-1, 3, int(output.size()[1] / 3))
        output1, output2, output3 = output[:, 0, :], output[:, 1, :], output[:, 2, :]
        return (output1, output2, output3)


def get_network():
    return TripDenseNet
