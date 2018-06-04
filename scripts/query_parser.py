#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

RE_INSTRUCTION = re.compile(r'^([a-zA-Z]+)\s+.+\s+FROM') # SELECT (Assuming *)

RE_COLUMNS = re.compile(r'^[a-z]+\s+([a-zA-Z, ]+)\s+FROM') # tytul, rezyser

RE_TABLE_NAME = re.compile(r'FROM\s+([a-zA-Z]+)(\s+WHERE)*') # filmy

RE_CONSTR_EXPR = re.compile(r'WHERE\s+(.+)')
RE_FEATURE = re.compile(r'WHERE\s+([a-zA-Z]+)') # czas
RE_CONSTRAINT = re.compile(r'WHERE\s+(.*)') # krótki

CONJUNCTIONS = ['AND', 'OR', 'NOT']


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
        pass

    def split_constr_expr(self, expr):
        """From 'czas krótki AND budzet niski AND rok_produkcji późny'
           obtain ['czas krótki', 'AND', 'budzet niski', 'AND', 'rok_produkcji późny']
        """
        delimiters = '|'.join(CONJUNCTIONS)
        constraints = re.split(delimiters, expr)
        conj_in_expr = []
        for word in expr.split():
            if word in CONJUNCTIONS:
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
            instruction = RE_INSTRUCTION.search(user_query).group(1)
            #print(instruction)
            table_name = RE_TABLE_NAME.search(user_query).group(1)
            #print(table_name)
            feature = RE_FEATURE.search(user_query).group(1)
            #print(feature)
            constraint = RE_CONSTRAINT.search(user_query).group(1)
            #print(constraint)
        except AttributeError:
            print('Invalid query. Exiting.')
            sys.exit(1)
        return instruction, table_name, feature, constraint
