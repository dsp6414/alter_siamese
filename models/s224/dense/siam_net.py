import torch

from models.s224.dense.net import DenseNet


class SiamDenseNet(DenseNet):
    def forward(self, (input1, input2)):
        x = torch.cat([input1, input2], dim=1)
        output = self.forward_once(x)
        output = output.view(-1, 2, int(output.size()[1] / 2))
        output1, output2 = output[:, 0, :], output[:, 1, :]
        return (output1, output2)


def get_network():
    return SiamDenseNet
