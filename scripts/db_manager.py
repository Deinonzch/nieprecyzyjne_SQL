#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2


def execute_query(query):
    """
    """
    try:
        conn=psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
    except:
        print('Failed to connect to the database.')
        return

    cur = conn.cursor()
    try:
        cur.execute(query)
    except:
        print('Failed to execute query.')

    table = cur.fetchall()
    return table


def write_to_file(table, fname):
    """Write to file
    """
    with open(fname, 'w') as table_f:
        for row in table:
            table_f.write('{}\n'.format(row))


def print_table(table):
    """
    """
    print()
    for i, row in enumerate(table):
        print('\t{}'.format(row))
        if i == 15:
            break
    print('\t...\n')


def retrieve_table(table_name, fname):
    """Retrieve requested table
    """
    query = 'SELECT * FROM {}'.format(table_name)
    table = execute_query(query)
    write_to_file(table, fname)


def execute_directly(query, fname):
    try:
        table = execute_query(query)
        write_to_file(table, fname)
        print_table(table)
        return 1
    except:
        return 0
