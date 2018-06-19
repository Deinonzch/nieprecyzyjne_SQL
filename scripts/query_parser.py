#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys


class QueryParser(object):

    def __init__(self):
        self.RE_INSTRUCTION = re.compile(r'^([a-zA-Z]+)\s+.+\s+FROM')
        self.RE_FUNCTION = re.compile(r'^[a-zA-Z]+\s+([a-zA-Z]*\()*.*\s+FROM')
        self.RE_COLUMNS = re.compile(r'^[a-zA-Z]+\s+([a-zA-Z]*\()*([a-zA-Z,* ]*).*\s+FROM')
        self.RE_TABLE_NAME = re.compile(r'FROM\s+([a-zA-Z]+)')

        self.RE_CONSTRAINT = re.compile(r'^\s*([a-zA-Z]+)\s+(is|==)\s+([a-zA-Z]+)\s*$')

        #self.CONJUNCTIONS = ['AND', 'OR', 'NOT']


    #TODO: Implement parsing more complex constraints (with OR and NOT)
    '''def split_constr_expr(self, expr):
        delimiters = '|'.join(self.CONJUNCTIONS)
        constraints = re.split(delimiters, expr)
        conj_in_expr = []
        for word in expr.split():
            if word in self.CONJUNCTIONS:
                conj_in_expr.append(word)
        return constraints, conj_in_expr'''


    def validate_query(self, query):
        """Validate query
        """
        if query.function and len(query.columns) > 1:
            print('Invalid query: too many function arguments. Exiting.')
            sys.exit(1)


    def parse_query(self, query, user_query):
        """Parse user query
        """
        try:
            query.whole_expr = user_query
            query.instr_expr = re.split('WHERE', user_query)[0].strip()
            query.constr_expr = re.split('WHERE', user_query)[1].strip()
    
            query.instruction = self.RE_INSTRUCTION.search(query.instr_expr).group(1)
            
            function = self.RE_FUNCTION.search(query.instr_expr).group(1)
            if function:
                query.function = function.strip('(')
            else:
                query.function = ''

            query.columns = [col.strip() for col in self.RE_COLUMNS.search(query.instr_expr).group(2).split(',')]

            query.table_name = self.RE_TABLE_NAME.search(query.instr_expr).group(1)

            constraints = query.constr_expr.split('AND')
            for constraint in constraints:
                feature = self.RE_CONSTRAINT.search(constraint).group(1)
                value = self.RE_CONSTRAINT.search(constraint).group(3)
                constraint_dict = {'feature': feature, 'value': value}
                query.constraints.append(constraint_dict)
        except:
            print('Failed to parse query. Exiting.')
            sys.exit(1)
