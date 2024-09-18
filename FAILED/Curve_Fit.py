#!/usr/bin/python
# -*- coding: utf-8 -*-
from numbers import Number
from symtable import Function
import random
E = 2.71828182845905
PI = 3.14159265358979

# exp
exp_accuracy = 1                  #
exp_f = lambda x: 2 * x           #
exp_section = (0, 1)              #
exp_step = 0.001                  #
exp_length = 10                   #
exp_lengthrange = 20              #
exp_coefficientrange = (-10, 10)  #
exp_times = 1000                  #

# cls
class Data_line(object):
    def __init__(self, f: list[Number], score: int):
        self.f = f
        self.score = score

    def output(self):
        return [self.f, self.score]

# func
def func_floatrange(a: Number, b: Number, step: Number) -> list:
    _l = []
    _s = a
    while _s <= b:
        _l.append(_s)
        _s += step
    return _l


def func_translate(f: list[Number]) -> Function:
    def _f(x: Number) -> Number:
        __s = 0
        for __i, __y in enumerate(f):
            __s += __y * x**__i
        return __s
    return _f


def func_judge(x: Data_line) -> Data_line:
    _f = func_translate(x.f)
    _s_dataf = 0
    _s_expf = 0
    _s_differ = 0
    for _y in func_floatrange(exp_section[0], exp_section[1], exp_step):
        _s_dataf = _f(_y)
        _s_expf = exp_f(_y)
        _s_differ += abs(_s_expf - _s_dataf)
    if _s_differ <= exp_accuracy:
        x.score = exp_length
    x.score -= len(x.f)
    return x


def func_generate():
    _n = random.randint(1, exp_lengthrange)
    _l = [random.uniform(exp_coefficientrange[0],
                         exp_coefficientrange[1]) for i in range(_n)]
    return Data_line(f=_l, score=0)


# program
l = [func_generate() for i in range(exp_times)]
for i, x in enumerate(l):
    l[i] = func_judge(x)
for x in l:
    if x.score >= 0:
        print(x.output())
