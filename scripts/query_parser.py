#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys


class QueryParser(object):

    def __init__(self):
        self.RE_INSTRUCTION = re.compile(r'^([a-zA-Z]+)\s+.+\s+[FROM|from]')
        self.RE_FUNCTION = re.compile(r'^[a-zA-Z]+\s+([a-zA-Z]*\()*.*\s+[FROM|from]')
        self.RE_COLUMNS = re.compile(r'^[a-zA-Z]+\s+([a-zA-Z]*\()*([a-zA-Z,* ]*).*\s+[FROM|from]')
        self.RE_TABLE_NAME = re.compile(r'[FROM|from]\s+([a-zA-Z]+)')

        #TODO: Parsing when only some of constraints are fuzzy
        self.RE_CONSTRAINT = re.compile(r'^\s*([a-zA-Z]+)\s+(is|==|!=)\s+([NOT|not]*\s*[a-zA-Z]+)\s*$')


    def validate_query(self, query):
        """Validate query
        """
        if query.function and len(query.columns) > 1:
            print('Invalid query: too many function arguments. Exiting.')
            sys.exit(1)


    def parse_constr_expr(self, query):
        """Parse constraint expression
        """
        constraints = re.split('AND|OR', query.constr_expr)
        if 'OR' in query.constr_expr:
            query.conjunction = 'OR'
        for constraint in constraints:
            feature = self.RE_CONSTRAINT.search(constraint).group(1)
            value = self.RE_CONSTRAINT.search(constraint).group(3).lower()
            if 'not' in value:
                polarity = False
                value = value.replace('not', '').strip()
            else:
                polarity = True
            constraint_dict = {'feature': feature, 'value': value, 'polarity': polarity}
            query.constraints.append(constraint_dict)


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

            self.parse_constr_expr(query)
        except ImportError:
            print('Failed to parse query. Exiting.')
            sys.exit(1)
