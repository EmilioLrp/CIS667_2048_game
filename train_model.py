import pickle
import src.control.conv_nn as conv_nn
import torch as tr
import os
import numpy as np
import time

def shuffle_data(size, x, y):
    shuffle = np.random.permutation(range(len(x)))
    split = int(len(x) / 10)
    train, test = shuffle[:-split], shuffle[-split:]
    x_train_raw = [x[i] for i in train]
    x_test_raw = [x[i] for i in test]
    y_train_raw = [y[i] for i in train]
    y_test_raw = [y[i] for i in test]
    x_train = [tr.tensor(i).reshape((1, 1, size, size)).float() for i in x_train_raw]
    x_test = [tr.tensor(i).reshape((1, 1, size, size)).float() for i in x_test_raw]
    y_train = [tr.tensor(j).float() for j in y_train_raw]
    y_test = [tr.tensor(j).float() for j in y_test_raw]
    return x_train, x_test, y_train, y_test


def train(size, goal):
    file1 = os.path.dirname(os.path.abspath(__file__)) + "/data/board_size_%d_goal_%d_train.dat" % (size, goal)
    model_file = os.path.dirname(os.path.abspath(__file__)) + "/model/board_size_%d_goal_%d_model.mod" % (size, goal)
    train_error_file = "size_%d_goal_%d_train_error.txt" % (size, goal)
    test_error_file = "size_%d_goal_%d_test_error.txt" % (size, goal)
    with open(file1, 'rb') as f1:
        (x, y) = pickle.load(f1)

    x_train, x_test, y_train, y_test = shuffle_data(size, x, y)
    model = conv_nn.NNModel(size)
    #optim = tr.optim.Adam(model.parameters())
    
    # optim = tr.optim.Adamax(model.parameters())
    optim = tr.optim.Adagrad(model.parameters())
    for epoch in range(100):
        start = time.time()
        for i in range(len(x_train)):
            input = x_train[i]
            output = y_train[i]
            conv_nn.train(model, optim, input, output)

        train_loss = conv_nn.calculate_loss(model, x_train, y_train)
        test_loss = conv_nn.calculate_loss(model, x_test, y_test)
        train_loss_str = "epoch: %d, loss: %s\n" % (epoch, str(train_loss))
        test_loss_str = "epoch: %d, loss: %s\n" % (epoch, str(test_loss))

        with open(train_error_file, 'a') as f1:
            f1.write(train_loss_str)
            f1.flush()

        with open(test_error_file, 'a') as f2:
            f2.write(test_loss_str)
            f2.flush()
        end = time.time()
        print("size %d goal %d epoch %d train done, time: %s" % (size, goal, epoch, str(end-start)))

    tr.save(model.state_dict(), model_file)


if __name__ == '__main__':
    game_size = [(3, 128), (3, 256), (4, 512), (4, 1024), (4, 2048)]
    # game_size = [(3, 256)]
    for s,g in game_size:
        train(s, g)
        print("size %d train done" % s)
