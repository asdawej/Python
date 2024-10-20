# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import random as rd
from decimal import Decimal as Deci
from math import ceil
from numbers import Real
from typing import Callable, Iterable, NoReturn

import numpy as np

__author__ = 'asdawej'

__date__ = '2023.2.4'

__doc__ = '''
=======================================================================
一个随机数生成器学习模型及其API.\n
主要部分为类 RandomLearning, 通过下面的参数初始化:\n
- 学习目标生成器 target_rd.\n
- 为目标生成器提供的参数 target_arg.\n
- 学习区间 limits (默认为[-5, 5]).\n
- 拟合精度 epsilon (默认为0.1).\n
通过 RandomLearning.learn, 你可以操控它的学习进程.\n
调用只需要在实例后面填一对小括号即可.
=======================================================================
类 RandomLearning 参数说明:\n
- target_rd:
    Callable[..., Real], 学习目标生成器\n
- target_arg:
    tuple, 为目标生成器提供的参数\n
- limits:
    list[Deci, Deci], 学习区间, [0]为左边界, [1]为右边界\n
- epsilon:
    Deci, 拟合精度, 学习结果应当在该长度的子区间内与目标相拟合\n
- groups:
    Deci, 根据精度确定的学习子区间数目\n
- length:
    Deci, 子区间长度\n
- weight:
    np.ndarray, 权重向量, 负责记录各个子区间的分布权重\n
- cdf:
    np.ndarray, 对权重求累积和, 前后加上0和1
=======================================================================
'''


class RandomLearning(object):
    def __init__(
        self,
        target_rd: Callable[..., Real],
        target_arg: tuple,
        limits: Iterable[Real, Real] = None,
        epsilon: Real = None
    ):
        self.target_rd: Callable[..., Real] = target_rd

        self.target_arg: tuple = target_arg

        if not limits:
            self.limits: list[Deci, Deci] = [Deci(-5), Deci(5)]
        else:
            if limits[1] <= limits[0]:
                raise ValueError('Wrong limits')
            self.limits: list[Deci, Deci] = [Deci(limits[0]), Deci(limits[1])]

        if not epsilon:
            self.epsilon: Deci = Deci(0.1)
        else:
            if epsilon >= self.limits[1] - self.limits[0]:
                raise ValueError('Epsilon too big')
            self.epsilon: Deci = Deci(epsilon)

        self.groups: Deci = Deci(ceil((self.limits[1] - self.limits[0]) / self.epsilon))

        self.length: Deci = (self.limits[1] - self.limits[0]) / self.groups

        self.weight: np.ndarray = np.ones(int(self.groups), dtype=Deci) / self.groups

        self.cdf: np.ndarray = np.insert(
            np.cumsum(self.weight), 0,
            np.array(Deci(0))
        )

    def __call__(self) -> Real:
        _rdflag = Deci(rd.random())
        _groupidx = Deci(int(np.argwhere(_rdflag < self.cdf)[0][0]) - 1)
        return rd.uniform(
            float(self.limits[0] + (_groupidx - 1) * self.length),
            float(self.limits[0] + _groupidx * self.length)
        )

    def learn(self, n: int) -> NoReturn:
        if n < 1:
            raise ValueError('Wrong loop times')
        _count_result = np.zeros(int(self.groups), dtype=Deci)
        for _ in range(n):
            _rdresult = Deci(self.target_rd(*self.target_arg))
            while _rdresult >= self.limits[1] or _rdresult < self.limits[0]:
                _rdresult = Deci(self.target_rd(*self.target_arg))
            _count_result[int((_rdresult - self.limits[0]) / self.length)] += 1
        _count_result: np.ndarray = _count_result / Deci(n)
        self.weight: np.ndarray = (self.weight + _count_result) / Deci(2)
        self.cdf[1:] = np.cumsum(self.weight)
