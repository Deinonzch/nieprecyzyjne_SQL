#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from collections import OrderedDict


class Query(object):

    def __init__(self):
        self.whole_expr = ''
        self.instr_expr = ''
        self.constr_expr = ''

        self.instruction = ''
        self.function = ''
        self.columns = []
        self.table_name = ''

        self.constraints = []


    def __str__(self):
        dictionary = OrderedDict([
            ('whole_expr', self.whole_expr),
            ('instr_expr', self.instr_expr),
            ('constr_expr', self.constr_expr),
            ('instruction', self.instruction),
            ('function', self.function),
            ('columns', self.columns),
            ('table_name', self.table_name),
            ('constraints', self.constraints)
        ])
        return (json.dumps(dictionary, indent=4, ensure_ascii=False))
