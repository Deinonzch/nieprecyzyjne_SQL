#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from query_parser import QueryParser
from fuzzy_manager import FuzzyManager
from table_manager import TableManager
from db_manager import DBManager

DEFAULT_THRESHOLD = 0.5

YES_ANSWERS = ['y', 'yes']
NO_ANSWERS = ['n', 'no']

FCL_FILE = 'files/user_definitions.fcl'
IN_TABLE_FILE = 'files/tmp_in_table.tsv'
OUT_TABLE_FILE = 'files/tmp_out_tuples.tsv'
OUTPUT_FILE = 'files/output.tsv'


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
    print('Fill in \'files/user_definitions.fcl\' file.')
    input('Press enter to continue ...')
    print('Variables and terms specified.')
    thr = ask_for_threshold()
    print('Type your query:')
    query = input('--> ')
    print('Processing your query ...')
    return thr, query


def process_fuzzy_query(user_query, threshold, db_mgr):
    """Process query with fuzzy constraints
    """
    parser = QueryParser()
    fuzzy_mgr = FuzzyManager()
    table_mgr = TableManager()

    #  Parse user query
    print('\nParsing query ...')
    instruction, table_name, feature, constraint = parser.parse_query(user_query)
    print('Query parsed.')

    #  Retrieve requested table
    print('\nRetrieving requested table from the database ...')
    db_mgr.retrieve_table(table_name, IN_TABLE_FILE)
    print('Table retrieved and saved to \'{}\' file.'.format(IN_TABLE_FILE))

    #  Parse constraint and obtain an interval
    print('\nParsing constraint from the query ...')
    interval = fuzzy_mgr.parse_constraint(feature, constraint, FCL_FILE)
    print('Constraint parsed. Corresponding interval obtained: {}.'.format(interval))

    #  Search for tuples
    print('\nExtracting tuples that meet the requirement ...')
    table_mgr.extract_tuples(feature, interval, IN_TABLE_FILE, OUT_TABLE_FILE)
    print('Tuples extracted and saved to \'{}\' file.'.format(OUT_TABLE_FILE))

    #  Parse and execute instruction
    print('\nExecuting instruction ...')
    table_mgr.execute_instruction(instruction, OUT_TABLE_FILE, OUTPUT_FILE)
    print('Instruction executed. Output saved to \'{}\' file.'.format(OUTPUT_FILE))


def main():
    """Main function
    """
    #  Ask user for input
    #threshold, user_query = ask_for_input()

    threshold = 0.5
    user_query = 'SELECT * FROM pokemon WHERE attack > 35'
    #user_query = 'SELECT * FROM pokemon WHERE attack is strong'

    #  Try to execute as an ordinary sql query
    #  If failure, process query with fuzzy constraints
    print('\nTrying to execute query directly ...')
    db_mgr = DBManager()
    if db_mgr.execute_directly(user_query, IN_TABLE_FILE):
        print('Query executed directly. Exiting.')
        sys.exit(1)
    else:
        print('Processing query with fuzzy constraints ...')
        process_fuzzy_query(user_query, threshold, db_mgr)


if __name__ == '__main__':
    main()
