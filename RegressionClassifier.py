__date__ = '2024.10.20'

__author__ = 'asdawej'

__doc__ = '使用二分类器解线性回归问题'

import random as rd

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch import nn, optim
import numpy as np


class SVM(nn.Module):
    '支持向量机'

    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(2, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)


model = SVM()
def criterion(x, y): return torch.mean(F.relu(1 - x * y))


opt = optim.Adam(model.parameters())

rd.seed(2024)
DATA_K = 2
DATA_B = 1
DATA_X_LIMIT = [-10, 10]
DATA_NUM = 100
NOISE_SIGMA = 1
LR = 0.01
XSI = 0.5
NUM_EPOCHS = 1000

data = torch.zeros([DATA_NUM, 2])
data[:, 0] = torch.Tensor([rd.uniform(*DATA_X_LIMIT) for _ in range(DATA_NUM)])
noise = torch.Tensor([rd.gauss(0, NOISE_SIGMA) for _ in range(DATA_NUM)])
data[:, 1] = data[:, 0] * DATA_K + DATA_B + noise
labels = torch.Tensor([(-1)**i for i in range(DATA_NUM)])

for epoch in range(NUM_EPOCHS):
    opt.zero_grad()
    outputs = model(data)
    param_w: list[list[float]] = model.linear.weight.tolist()
    param_w1, param_w2 = param_w[0]
    loss = XSI * criterion(outputs, labels) + 0.5 * (param_w1**2 + param_w2**2)
    line_loss = torch.sum(outputs**2)
    loss.backward()
    opt.step()
    if epoch % 50 == 49:
        param_b = model.linear.bias.item()
        line_k = -param_w1 / param_w2
        line_b = -param_b / param_w2
        print(f'{epoch:2d}: {loss:.2f}, {line_loss:.2f}, {line_k:.3f}, {line_b:.3f}')

line_x = np.arange(*DATA_X_LIMIT, 0.1)
line_y = line_x * line_k + line_b
plt.plot(line_x, line_y)
plt.scatter(data[:, 0].detach(), data[:, 1].detach(), 0.5)
plt.grid(True)
plt.show()
