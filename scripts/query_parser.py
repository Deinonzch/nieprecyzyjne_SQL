#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys


class Query(object):

    def __init__(self):
        self.whole_expr = ''
        self.instr_expr = ''
        self.constr_expr = ''

        self.instruction = ''
        self.columns = []
        self.table = ''

        self.constr_list = []


class QueryParser(object):

    def __init__(self):
        self.RE_INSTRUCTION = re.compile(r'^([a-zA-Z]+)\s+.+\s+FROM') # SELECT (Assuming *)

        self.RE_COLUMNS = re.compile(r'^[a-z]+\s+([a-zA-Z, ]+)\s+FROM') # tytul, rezyser

        self.RE_TABLE_NAME = re.compile(r'FROM\s+([a-zA-Z]+)(\s+WHERE)*') # filmy

        self.RE_CONSTR_EXPR = re.compile(r'WHERE\s+(.+)')
        self.RE_FEATURE = re.compile(r'WHERE\s+([a-zA-Z]+)') # czas
        self.RE_CONSTRAINT = re.compile(r'WHERE\s+(.*)') # krótki

        self.CONJUNCTIONS = ['AND', 'OR', 'NOT']


    def split_constr_expr(self, expr):
        """From 'czas krótki AND budzet niski AND rok_produkcji późny'
           obtain ['czas krótki', 'AND', 'budzet niski', 'AND', 'rok_produkcji późny']
        """
        delimiters = '|'.join(self.CONJUNCTIONS)
        constraints = re.split(delimiters, expr)
        conj_in_expr = []
        for word in expr.split():
            if word in self.CONJUNCTIONS:
                conj_in_expr.append(word)
        return constraints, conj_in_expr


    def parse_query(self, user_query):
        """Parse user query
        """
        query = Query()

        query.whole_expr = user_query
        query.instr_expr = re.split('WHERE', user_query)[0].strip()
        query.constr_expr = re.split('WHERE', user_query)[1].strip()
    
        print(query.instr_expr)
        print(query.constr_expr)

        #try:
        #    constr_expr = RE_CONSTR_EXPR.search(query).group(1)
        #except AttributeError:
        #    print('Attribute error')
        #constraints, conj_in_expr = split_constr_expr(constr_expr)

        try:
            instruction = self.RE_INSTRUCTION.search(user_query).group(1)
            #print(instruction)
            table_name = self.RE_TABLE_NAME.search(user_query).group(1)
            #print(table_name)
            feature = self.RE_FEATURE.search(user_query).group(1)
            #print(feature)
            constraint = self.RE_CONSTRAINT.search(user_query).group(1)
            #print(constraint)
        except AttributeError:
            print('Invalid query. Exiting.')
            sys.exit(1)
        return instruction, table_name, feature, constraint
