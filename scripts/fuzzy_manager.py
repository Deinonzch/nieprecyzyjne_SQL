#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import re


class LingVar(object):

    def __init__(self):
        self.name = ''
        self.term_dicts = []

    def __str__(self):
        return 'name: {}'.format(self.name) + '\nterms: {}'.format(self.term_dicts)


class FuzzyManager(object):

    def __init__(self):
        self.RE_VARIABLE = re.compile(r'FUZZIFY\s+(.+)')
        self.RE_TERM = re.compile(r'\s+TERM\s+(.+)\s+:=')
        self.RE_VALUES = re.compile(r':=\s+(.+)')
        self.RE_VALUE = re.compile(r'\(([0-9]+),')

    def parse_values(self, string):
        """Parse values
        """
        vals_str = self.RE_VALUES.search(string).group(1)
        return [int(val) for val in self.RE_VALUE.findall(vals_str)]


    def parse_fcl(self, fcl_file):
        """Parse FCL file
        """
        lingVars = [] 
        with open(fcl_file, 'r') as fcl_f:
            for line in fcl_f:
                if line.startswith('FUZZIFY'):
                    lingVar = LingVar()
                    lingVar.name = self.RE_VARIABLE.search(line).group(1)
                elif 'TERM' in line:
                    term = self.RE_TERM.search(line).group(1)
                    values = self.parse_values(line)
                    term_dict = {'term': term, 'values': values}
                    lingVar.term_dicts.append(term_dict)
                elif 'END_FUZZIFY' in line:
                    lingVars.append(lingVar)
        return lingVars


    def find_min_max(self, lingVar):
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
 

    def define_skfuzzy_var(self, threshold, lingVar):
        """Define variable using skfuzzy syntax
        """
        min_val, max_val = self.find_min_max(lingVar)
        var = ctrl.Antecedent(np.arange(min_val, max_val, 1), lingVar.name)
        for term_dict in lingVar.term_dicts:
            values = fuzz.trimf(var.universe, term_dict['values'])
            thr_values = []
            for value in values:
                if value < threshold:
                    thr_values.append(0)
                else:
                    thr_values.append(value)
            var[term_dict['term']] = thr_values
        var.view()
        input("Press Enter to continue...")
        return var


    def parse_constraint(self, feature, value, threshold, fcl_file):
        """Parse constraint and obtain an interval
        """
        interval = None
        lingVars = self.parse_fcl(fcl_file)
        for lingVar in lingVars:
            if lingVar.name == feature:
                skfuzzy_var = self.define_skfuzzy_var(threshold, lingVar)
                for term_dict in lingVar.term_dicts:
                    if term_dict['term'] == value:
                        interval_beg = min(term_dict['values'])
                        interval_end = max(term_dict['values'])
                        interval = tuple((interval_beg, interval_end))
        return interval


    def parse_constraints(self, constraints, threshold, fcl_file):
        """Parse constraints
        """
        for constraint in constraints:
            interval = self.parse_constraint(constraint['feature'], constraint['value'], threshold, fcl_file)
            constraint['interval'] = interval
            if not interval:
                print('Failed to obtain interval for feature'
                      + ' \'{}\' and value \'{}\'.'.format(constraint['feature'], constraint['value'])
                      + ' Constraint will be ignored.')
