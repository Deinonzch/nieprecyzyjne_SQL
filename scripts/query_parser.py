#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

RE_INSTRUCTION = re.compile(r'([a-zA-Z]+)\s+.+\s+FROM') # SELECT (Assuming *)
RE_TABLE_NAME = re.compile(r'FROM\s+([a-zA-Z]+)\s+WHERE') # filmy
RE_FEATURE = re.compile(r'WHERE\s+([a-zA-Z]+)') # czas
RE_CONSTRAINT = re.compile(r'WHERE\s+.+\s(.*)') # krótki

CONJUNCTIONS = ['and', 'or', 'not']


def parse_query(user_query):
    """Parse user query
    """
    try:
        instruction = RE_INSTRUCTION.search(user_query).group(1)
        table_name = RE_TABLE_NAME.search(user_query).group(1)
        feature = RE_FEATURE.search(user_query).group(1)
        constraint = RE_CONSTRAINT.search(user_query).group(1)
    except AttributeError:
        print('Invalid query. Exiting.')
        sys.exit(1)
    return instruction, table_name, feature, constraint
