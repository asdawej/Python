# !usr/bin/env python
# -*- coding: utf-8 -*-

import easygui as eg
__author__ = 'asdawej'
__date__ = '2022.9.20'

'''
Hello!
This is a program I use for learning some modules.
Tired of searching docs, I made this to remember the classes, methods and args of them.
You will soon know that this is an excellent program to keep all of them!
'''


TITLE = 'Modules Lines Dictionary-by asdawej'
CHOICES_1 = ['Search', 'Revise', 'Add']
CHOICES_2_ADD = ['Module', 'Line']


def _pack_list(_l: list[str]) -> list[tuple[str]]:
    _i = 0
    _ll = []
    _s = ''
    for _x in _l:
        if _i == 0:
            _s = _x
            _i = 1
        elif _i == 1:
            _ll.append((_s, _x))
            _i = 0
    return _ll


def _unpack_list(_l: list[tuple[str]]) -> list[str]:
    _ll = []
    for _x in _l:
        _ll.append(_x[0])
        _ll.append(_x[1])
    return _ll


while True:
    choice_1 = eg.choicebox(
        msg='Please choose a operation:', title=TITLE, choices=CHOICES_1)
    with open('ModuleNames.txt', mode='r', encoding='utf-8') as ModuleNames:
        list_ModuleNames = ModuleNames.readlines()


    def search():
        choice_2 = eg.choicebox(
            msg='Please choose a module:', title=TITLE, choices=list_ModuleNames)
        with open(choice_2+'.txt', mode='r', encoding='utf-8') as Module:
            list_init_mod = _pack_list(Module.readlines())
            dict_init_mod = dict(list_init_mod)
            print(dict_init_mod[input('The name:')])


    def revise():
        choice_2 = eg.choicebox(
            msg='Please choose a module:', title=TITLE, choices=list_ModuleNames)
        with open(choice_2+'.txt', mode='r', encoding='utf-8') as Module:
            list_init_mod = _pack_list(Module.readlines())
        choice_3 = input('The name:')
        revision = input('New description:')
        for i, x in list_init_mod:
            if x[0] == choice_3:
                list_init_mod[i] = (choice_3, revision)
        with open(choice_2+'.txt', mode='w', encoding='utf-8') as Module:
            Module.writelines([x+'\n' for x in _unpack_list(list_init_mod)])


    def add():
        choice_2_add = eg.choicebox(
            msg='Is a module or a line?:', title=TITLE, choices=CHOICES_2_ADD)


        def add_module():
            module_name = input('The name of the module:')
            with open(module_name+'.txt', 'x'):
                pass
            with open('ModuleNames.txt', mode='r', encoding='utf-8') as _ModuleNames:
                _list_ModuleNames = _ModuleNames.readlines()
            _list_ModuleNames.append(module_name)
            with open('ModuleNames.txt', mode='w', encoding='utf-8') as _ModuleNames:
                _ModuleNames.writelines([x+'\n' for x in _list_ModuleNames])


        def add_line():
            module_name = input('The name of the module:')
            line_name = input('Please enter the name:')
            line_description = input('Please enter the description:')
            with open(module_name+'.txt', mode='r', encoding='utf-8') as Module:
                list_init_mod = _pack_list(Module.readlines())
            list_init_mod.append((line_name, line_description))
            with open(module_name+'.txt', mode='w', encoding='utf-8') as Module:
                Module.writelines(
                    [x+'\n' for x in _unpack_list(list_init_mod)])
        {CHOICES_2_ADD[0]: add_module, CHOICES_2_ADD[1]            : add_line}[choice_2_add]()

    {CHOICES_1[0]: search, CHOICES_1[1]: revise, CHOICES_1[2]: add}[choice_1]()
