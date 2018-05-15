#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def write_to_file(table, fname):
    """Write to file
    """
    with open(fname, 'w') as table_f:
        for row in table:
            table_f.write('{}\n'.format(row))


def load_from_db(table_name):
    """Load table from the database
    """
    table = [1,2,3,4,5]
    return table


def retrieve_table(table_name, fname):
    """Retrieve requested table
    """
    table = load_from_db(table_name)
    write_to_file(table, fname)
