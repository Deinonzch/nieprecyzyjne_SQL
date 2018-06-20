#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

from query import Query
from query_parser import QueryParser
from fuzzy_manager import FuzzyManager
from table_manager import TableManager
from db_manager import DBManager

DEFAULT_THRESHOLD = 0.5

YES_ANSWERS = ['y', 'yes']
NO_ANSWERS = ['n', 'no']

FCL_FILE = 'files/user_definitions.fcl'
IN_FILE = 'files/in.tsv'
TMP_FILE = 'files/tmp.tsv'
OUT_FILE = 'files/out.tsv'


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
    query = Query()
    parser = QueryParser()
    fuzzy_mgr = FuzzyManager()
    table_mgr = TableManager()

    #  Parse user query
    print('\nParsing query ...')
    parser.parse_query(query, user_query)
    print(query)
    print('Query parsed.')

    #  Verify correctness of the query
    print('Validating query ...')
    parser.validate_query(query)
    print('Query validated. No errors found.')

    #  Retrieve requested table
    print('\nRetrieving requested table from the database ...')
    db_mgr.retrieve_table(query.table_name, IN_FILE)
    print('Table retrieved and saved to \'{}\' file.'.format(IN_FILE))

    #  Parse constraints and obtain intervals
    print('\nParsing constraints from the query and obtaining intervals ...')
    fuzzy_mgr.parse_constraints(query.constraints, threshold, FCL_FILE)
    print(json.dumps(query.constraints, indent=4, ensure_ascii=False))
    print('Constraints parsed.')

    #  Search for tuples
    print('\nExtracting tuples that meet the requirement ...')
    table_mgr.extract_tuples(query.constraints, IN_FILE, TMP_FILE)
    print('Tuples extracted and saved to temporary files.')

    #  Parse and execute instruction with function
    print('\nExecuting instruction ...')
    table_mgr.execute_instruction(query.instruction, query.function, query.columns, TMP_FILE, OUT_FILE)
    print('Instruction executed. Output saved to \'{}\' file.'.format(OUT_FILE))


def main():
    """Main function
    """
    #  Ask user for input
    #threshold, user_query = ask_for_input()

    threshold = 0.8
    #user_query = 'SELECT * FROM pokemon WHERE attack > 35'
    #user_query = 'SELECT SUM(attack, defense, speed) FROM pokemon WHERE attack is strong AND defense is medium AND speed is slow'
    user_query = 'SELECT MAX(defense) FROM pokemon WHERE attack is strong AND defense is medium AND speed is not slow'
    #user_query = 'SELECT COUNT(attack) FROM pokemon WHERE attack is not weak'
    #user_query = 'SELECT * FROM pokemon WHERE attack is strong OR defense is medium OR speed is slow'


    #  Try to execute as an ordinary sql query
    #  If failure, process query with fuzzy constraints
    print('\nTrying to execute query directly ...')
    db_mgr = DBManager()
    if db_mgr.execute_directly(user_query, OUT_FILE):
        print('Query executed directly. Output saved to \'{}\' file. Exiting.'.format(OUT_FILE))
        sys.exit(1)
    else:
        process_fuzzy_query(user_query, threshold, db_mgr)


if __name__ == '__main__':
    main()
