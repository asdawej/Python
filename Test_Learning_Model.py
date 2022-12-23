#!/usr/bin/python
# -*- coding: utf-8 -*-

import random as RnDm


class Size:
    '''<1>
    m:  矩阵行数    /int/
    n:  矩阵列数    /int/
    '''

    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n


class Model:
    '''<1>
    epsilon:    模型调整程度            /float/
    arr:        模型矩阵                /list[list[float]]/
    size:       模型矩阵形状            /Size/
    goodlength: 被列为good的样本计数    /int/
    badlength:  被列为bad的样本计数     /int/
    goodmean:   被列为good的样本平均    /list[list[float]]/
    badlength:  被列为bad的样本平均     /list[list[float]]/
    '''

    def __init__(self, arr: list[list[float]], size: Size, epsilon: float):
        self.epsilon = epsilon
        self.arr = arr
        self.size = size
        self.goodlength = 0
        self.badlength = 0
        self.goodmean = [[0]*self.size.n]*self.size.m
        self.badmean = [[0]*self.size.n]*self.size.m

    def generate(self, x: list[float]) -> list[float]:
        '''<2>
        模型接受输入x, 模型输出
        '''
        if len(x) != self.size.n:
            raise TypeError
        y = [0]*self.size.m
        for i in range(self.size.n):
            for j in range(self.size.m):
                y[j] += x[i]*self.arr[j][i]
        return y

    def mean(self, new_arr: list[list[float]], good: bool):
        '''<2>
        输入带标记矩阵样本, 更新self.goodmean或self.badmean
        '''
        if good:
            for i in range(self.size.m):
                for j in range(self.size.n):
                    self.goodmean[i][j] = (
                        self.goodmean[i][j]*self.goodlength+new_arr[i][j])/(self.goodlength+1)
                    self.goodlength += 1
        else:
            for i in range(self.size.m):
                for j in range(self.size.n):
                    self.badmean[i][j] += (self.badmean[i][j] *
                                           self.badlength+new_arr[i][j])/(self.badlength+1)
                    self.badlength += 1

    def evolution(self, new_arr: list[list[float]], good: bool):
        '''<2>
        调用self.mean(), 然后和self.goodmean与self.badmean比较并调整self.arr
        '''
        self.mean(new_arr, good)
        for i in range(self.size.m):
            for j in range(self.size.n):
                if self.goodmean[i][j] < self.badmean[i][j]:
                    if self.arr[i][j] < self.goodmean[i][j]:
                        self.arr[i][j] += self.epsilon
                    else:
                        self.arr[i][j] -= self.epsilon
                elif self.goodmean[i][j] > self.badmean[i][j]:
                    if self.arr[i][j] > self.goodmean[i][j]:
                        self.arr[i][j] -= self.epsilon
                    else:
                        self.arr[i][j] += self.epsilon
                else:
                    if self.arr[i][j] > self.goodmean[i][j]:
                        self.arr[i][j] -= self.epsilon
                    elif self.arr[i][j] < self.goodmean[i][j]:
                        self.arr[i][j] += self.epsilon


'''<0>
EPSILON:    模型预期拟合精度    /float/
COUNT:      学习数据计数断点    /int/
'''
EPSILON = 1
COUNT = 100000


def test_model(x: list[float]) -> list[float]:
    '''<1>
    预期模型: [[1, 1]]
    '''
    return [x[0]+x[1]]


def check(model: Model, x: list[float], count_i: int):
    '''<1>
    测试model并调用model.evolution(), 满COUNT打印
    '''
    y = model.generate(x)
    y_test = test_model(x)
    if count_i == COUNT:
        print('Output y=', end='')
        print(y)
        print('Output y_test=', end='')
        print(y_test)
    if abs(y[0]-y_test[0]) <= EPSILON:
        model.evolution(new_arr=model.arr, good=True)
    else:
        model.evolution(new_arr=model.arr, good=False)
    if count_i == COUNT:
        print('Model arr: ')
        for i in range(model.size.m):
            print(model.arr[i])


if __name__ == '__main__':
    model = Model(arr=[[1, 1]], size=Size(m=1, n=2), epsilon=0.001)
    count_i = 0
    while True:
        x = [RnDm.uniform(-10000.0, 10000.0),
             RnDm.uniform(-10000.0, 10000.0)]  # 随机生成测试数据
        count_i += 1
        if count_i == COUNT:
            print('Input x=', end='')
            print(x)
        check(model, x, count_i)
        if count_i == COUNT:
            count_i = 0
            if int(input('Continue?[0/1]')) == 0:
                break
