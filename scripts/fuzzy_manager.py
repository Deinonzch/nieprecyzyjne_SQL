#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import re


RE_VARIABLE = re.compile(r'FUZZIFY\s+(.+)')
RE_TERM = re.compile(r'\s+TERM\s+(.+)\s+:=')
RE_VALUES = re.compile(r':=\s+(.+)')
RE_VALUE = re.compile(r'\(([0-9]+),')


class LingVar(object):
    def __init__(self):
        self.name = ''
        self.term_dicts = []

    def __str__(self):
        return 'name: {}'.format(self.name) + '\nterms: {}'.format(self.term_dicts)


def parse_values(string):
    """Parse values
    """
    vals_str = RE_VALUES.search(string).group(1)
    return [int(val) for val in RE_VALUE.findall(vals_str)]


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
                values = parse_values(line)
                term_dict = {'term': term, 'values': values}
                lingVar.term_dicts.append(term_dict)
            elif 'END_FUZZIFY' in line:
                lingVars.append(lingVar)
    return lingVars


def find_min_max(lingVar):
    """Find min and max values for terms
    """
    min_val = min(lingVar.term_dicts[0]['values'])
    max_val = max(lingVar.term_dicts[0]['values'])+1
    for term_dict in lingVar.term_dicts:
        min_tmp = min(term_dict['values'])
        max_tmp = max(term_dict['values'])+1
        if min_val > min_tmp:
            min_val = min_tmp
        if max_val < max_tmp:
            max_val = max_tmp
    return min_val, max_val


def define_skfuzzy_var(lingVar):
    """Define variable using skfuzzy syntax
    """
    min_val, max_val = find_min_max(lingVar)
    var = ctrl.Antecedent(np.arange(min_val, max_val, 1), lingVar.name)
    for term_dict in lingVar.term_dicts:
        var[term_dict['term']] = fuzz.trimf(var.universe, term_dict['values'])
    var.view()
    input("Press Enter to continue...")
    return var


def parse_constraint(feature, constraint, fcl_file):
    """Parse constraint
    """
    lingVars = parse_fcl(fcl_file)
    for lingVar in lingVars:
        if lingVar.name == feature:
            skfuzzy_var = define_skfuzzy_var(lingVar)
            for term_dict in lingVar.term_dicts:
                if term_dict['term'] == constraint:
                    interval_beg = min(term_dict['values'])
                    interval_end = max(term_dict['values'])
    interval = range(interval_beg, interval_end)
    return interval
