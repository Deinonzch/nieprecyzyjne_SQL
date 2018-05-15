#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from fuzzy_manager import parse_constraint
from db_manager import retrieve_table
from table_manager import extract_tuples
from table_manager import execute_instruction

DEFAULT_THRESHOLD = 0.5

YES_ANSWERS = ['y', 'yes']
NO_ANSWERS = ['n', 'no']

#SELECT * FROM filmy WHERE czas krótki

RE_INSTRUCTION = re.compile(r'([a-zA-Z]+)\s+.+\s+FROM') # SELECT (Assuming *)
RE_TABLE_NAME = re.compile(r'FROM\s+([a-zA-Z]+)\s+WHERE') # filmy
RE_FEATURE = re.compile(r'WHERE\s+([a-zA-Z]+)') # czas
RE_CONSTRAINT = re.compile(r'WHERE\s+.+\s(.*)') # krótki

FCL_FILE = 'user_definitions.fcl'
TABLE_FILE = '../tables/filmy.tsv'
TUPLES_FILE = 'tuples.tsv'
OUTPUT_FILE = 'output.tsv'


def ask_for_threshold():
    """Ask user to specify threshold
    """
    thr = DEFAULT_THRESHOLD
    answer = input('Would you like to specify threshold (y/n)? ').lower()
    if answer in YES_ANSWERS:
        thr = float(input('--> '))
        print('Threshold set with value {}.'.format(thr))
    elif answer in NO_ANSWERS:
        print('Threshold set with default value {}.'.format(DEFAULT_THRESHOLD))
    else:
        print('No proper answer given. Threshold set with default value {}.'.format(DEFAULT_THRESHOLD))
    return thr


def ask_for_input():
    """Ask user for input
    """
    print('Fill in \'user_definitions.fcl\' file with linguistic variable(s) and terms.')
    input('Press enter to continue ...')
    print('Variables and terms specified.')
    thr = ask_for_threshold()
    print('Type your query:')
    query = input('--> ')
    print('Processing your query ...')
    return thr, query


def main():
    """Main function
    """
    #  Ask user for input
    threshold, user_query = ask_for_input()

    #threshold = 0.5
    #user_query = 'SELECT * FROM filmy WHERE czas krótki'

    #  Extract values
    try:
        instruction = RE_INSTRUCTION.search(user_query).group(1)
        table_name = RE_TABLE_NAME.search(user_query).group(1)
        feature = RE_FEATURE.search(user_query).group(1)
        constraint = RE_CONSTRAINT.search(user_query).group(1)
    except AttributeError:
        print('Invalid query. Exiting.')
        sys.exit(1)

    #  Retrieve requested table
    '''print('\nRetrieving requested table from the database ...')
    retrieve_table(table_name, TABLE_FILE)
    print('Table retrieved and saved to \'{}\' file.'.format(TABLE_FILE))'''

    #  Parse constraint and obtain an interval
    print('\nParsing constraint from the query ...')
    interval = parse_constraint(feature, constraint, FCL_FILE)
    print('Constraint parsed. Corresponding interval obtained: {}.'.format(interval))

    #  Search for tuples
    print('\nExtracting tuples that meet the requirement ...')
    extract_tuples(feature, interval, TABLE_FILE, TUPLES_FILE)
    print('Tuples extracted and saved to \'{}\' file.'.format(TUPLES_FILE))

    #  Parse and execute instruction
    print('\nExecuting instruction ...')
    execute_instruction(instruction, TUPLES_FILE, OUTPUT_FILE)
    print('Instruction executed. Output saved to \'{}\' file.'.format(OUTPUT_FILE))


if __name__ == '__main__':
    main()
