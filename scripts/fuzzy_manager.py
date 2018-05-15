#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


RE_VARIABLE = re.compile(r'FUZZIFY\s+(.+)')
RE_TERM = re.compile(r'\s+TERM\s+(.+)\s+:=')
RE_VALUES = re.compile(r':=\s+(.+)')


class LingVar(object):
    def __init__(self):
        self.name = ''
        self.term_dicts = []

    def __str__(self):
        return 'name: {}'.format(self.name) + '\nterms: {}'.format(self.term_dicts)


def parse_fcl(fcl_file):
    """Parse FCL file
    """
    lingVars = [] 
    with open(fcl_file, 'r') as fcl_f:
        for line in fcl_f:
            if line.startswith('FUZZIFY'):
                lingVar = LingVar()
                lingVar.name = RE_VARIABLE.search(line).group(1)
            elif 'TERM' in line:
                term = RE_TERM.search(line).group(1)
                values = RE_VALUES.search(line).group(1)
                term_dict = {'term': term, 'values': values}
                lingVar.term_dicts.append(term_dict)
            elif 'END_FUZZIFY' in line:
                lingVars.append(lingVar)
    return lingVars


def parse_constraint(feature, constrainti, fcl_file):
    """Parse constraint
    """
    lingVars = parse_fcl(fcl_file)
    for var in lingVars:
        print(var)

    interval = (100, 111)
    return interval
