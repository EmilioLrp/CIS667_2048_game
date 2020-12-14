import torch as tr
import pickle
import numpy as np

ls = tr.nn.SmoothL1Loss()


class NNModel(tr.nn.Module):
    def __init__(self, size):
        super(NNModel, self).__init__()
        # self.conv = self._conv()
        self._kernel_1 = np.array([[1, 1]])
        self._kernel_2 = np.array([[1], [1]])
        self.conv_1 = self._conv(self._kernel_1)
        self.conv_2 = self._conv(self._kernel_2)
        self.flatten = tr.nn.Flatten()
        self.linear = tr.nn.Linear((size - 1) ** 2, 8)
        self.softmax = tr.nn.Softmax()

    def _conv(self, kernel):
        weight = tr.Tensor(kernel).reshape((1, 1, kernel.shape[0], kernel.shape[1])).float()
        weight.requires_grad = True
        model = tr.nn.Conv2d(1, 1, kernel_size=(2, 2), stride=1, bias=False)
        model.weight = tr.nn.Parameter(weight)
        return model

    def forward(self, x):
        # x = self.conv(x)
        x = self.conv_1(x)
        x = self.conv_2(x)
        x = self.flatten(x)
        x = self.linear(x)
        x = self.softmax(x)
        return x


# def loss_function(y, y_des):
#     diff = y - y_des
#     diff = tr.square(diff)
#     return tr.sum(diff)


def calculate_loss(model, xs, ys_des):
    loss = 0.
    for i in range(len(xs)):
        input = xs[i]
        label = ys_des[i]
        out = model(input)
        err = ls(out, label)
        loss += err.item()
    return loss / len(xs)


def optimization_step(optimizer, model, x, y_des):
    optimizer.zero_grad()
    y = model(x)
    loss = ls(y, y_des)
    loss.backward()
    optimizer.step()
    return y, loss


def train(model, optimizer, input, des_output):
    y_train, loss_train = optimization_step(optimizer=optimizer, model=model, x=input, y_des=des_output)
    return y_train, loss_train
