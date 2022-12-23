#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

# This column is the settings of experiment.
init_env = {
    'temperature': 20,
    'oxygen': 21,
    'water': 40,
    'enemy': 25,
    'food': 30
}
env_change = [-2, -1, 1, 2]
init_genes = {
    'heat resistance': 40,
    'cold resistance': 0,
    'oxygen consumption': 5,
    'water consumption': 30,
    'drought tolerance': 10,
    'defense': 40,
    'body build': 20
}
genes_change = [-2, -1, 1, 2]
init_quantity = 10
pop_growth_rate = 0.5

env = init_env

# For /Population/, it is a database of /Individual/ objects which go as keys to connect /Individual/ with procedure.


class Population(object):
    def __init__(self, name: str, individuals: list, quantity: int):
        self.name = name
        self.individuals = individuals
        self.quantity = quantity

    def multiply(self):
        _quantity = self.quantity
        _growth = int(_quantity*pop_growth_rate)
        self.quantity += _growth
        _d_genes = init_genes
        for x in self.individuals:
            for k in init_genes.keys():
                _d_genes[k] += x.genes[k]
        for k in init_genes:
            _d_genes[k] = _d_genes[k]//_quantity
        for i in range(_growth):
            self.individuals.append(Individual(genes=_d_genes, life=True))

    def iflife(self) -> bool:
        'pop off dead individual and check if the /Population/ is alive, to determine whether to kill the program'
        _index = []
        for i, x in enumerate(self.individuals):
            if not x.life:
                self.quantity -= 1
                _index.append(i)
        for i in _index[::-1]:
            self.individuals.pop(i)
        if self.quantity <= 0:
            print(self.name, 'dieout')
            return False
        else:
            return True
# For /Individual/, it is the object that we compare with the environment and do experiment with.


class Individual(object):
    def __init__(self, genes: dict, life: bool):
        self.genes = genes
        self.life = life

    def criteria(self) -> bool:
        'the criteria to determine the life of a creature individual'
        _iftem = self.genes['cold resistance'] <= env['temperature'] and env['temperature'] <= self.genes['heat resistance']
        _ifoxy = self.genes['oxygen consumption'] <= env['oxygen']
        _ifwat = self.genes['drought tolerance'] >= self.genes['water consumption']-env['water']
        _ifene = self.genes['defense'] >= env['enemy']
        _iffoo = self.genes['body build'] <= env['food']
        if _iftem and _ifoxy and _ifwat and _ifene and _iffoo:
            return False
        else:
            return True

    def iflife(self):
        'before /Population.iflife()/, check if the /Individual/ is alive, and revise /self.life/'
        if self.criteria():
            self.life = False


# programme
exp_pop = Population(
    name='exp_pop',
    individuals=[Individual(genes=init_genes, life=True)
                 for i in range(init_quantity)],
    quantity=init_quantity
)
gen_num = 0
while True:
    exp_pop.multiply()
    gen_num += 1
    for k in init_env.keys():
        env[k] += random.choice(env_change)
    for x in exp_pop.individuals:
        _body_build = x.genes['body build']
        for k in init_genes.keys():
            x.genes[k] += random.choice(genes_change)
        # /cold resistance/ may not bigger than /heat resistance/
        if x.genes['cold resistance'] > x.genes['heat resistance']:
            x.genes['cold resistance'], x.genes['heat resistance'] = x.genes['heat resistance'], x.genes['cold resistance']
        # /defense/ is related to /body build/
        if x.genes['body build'] > _body_build:
            x.genes['defense'] += 1
    for x in exp_pop.individuals:
        x.iflife()
    print(gen_num)
    if not exp_pop.iflife():
        break
    if input('check genes?[Y/N]') != 'Y':
        print([(i, x.genes) for i, x in enumerate(exp_pop.individuals)])
input('[Enter]')
