import torch as tr
import pickle


class NNModel(tr.nn.Module):
    def __init__(self, size):
        super(NNModel, self).__init__()
        self.conv = self._conv()
        self.flatten = tr.nn.Flatten()
        self.linear = tr.nn.Linear((size - 1) ** 2, 8)
        self.softmax = tr.nn.Softmax()

    def _conv(self):
        weight = tr.Tensor([[1, 1], [1, 1]]).reshape((1, 1, 2, 2)).float()
        weight.requires_grad = True
        model = tr.nn.Conv2d(1, 1, kernel_size=(2, 2), stride=1, bias=False)
        model.weight = tr.nn.Parameter(weight)
        return model

    def forward(self, x):
        x = self.conv(x)
        x = self.flatten(x)
        x = self.linear(x)
        x = self.softmax(x)
        return x


def loss_function(y, y_des):
    diff = y - y_des
    diff = tr.square(diff)
    return tr.sum(diff)


def calculate_loss(model, xs, ys_des):
    loss = 0.
    for i in range(len(xs)):
        input = xs[i]
        label = ys_des[i]
        out = model(input)
        err = loss_function(out, label)
        loss += err.item()
    return loss / len(xs)


def optimization_step(optimizer, model, x, y_des):
    optimizer.zero_grad()
    y = model(x)
    loss = loss_function(y, y_des)
    # y, loss = calculate_loss(model, x, y_des)
    loss.backward()
    optimizer.step()
    return y, loss


def train(model, optimizer, input, des_output):
    y_train, loss_train = optimization_step(optimizer=optimizer, model=model, x=input, y_des=des_output)
    return y_train, loss_train


