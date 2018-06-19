#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import csv


class DBManager(object):

    def __init__(self):
        pass

    def execute_query(self, query):
        """Connect to the database and execute query
        """
        try:
            conn=psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
        except:
            print('Failed to connect to the database.')
            return None

        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print('Failed to execute query.')
            return None

        db_list = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return db_list, column_names


    def write_to_file(self, table, col_names, fname):
        """Write to file
        """
        with open(fname,'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(col_names)
            for row in table:
                writer.writerow(row)


    def print_table(self, table):
        """Print retrieved table
        """
        print()
        for i, row in enumerate(table):
            print('\t{}'.format(row))
            if i == 15:
                break
        print('\t...\n')


    def retrieve_table(self, table_name, fname):
        """Retrieve requested table
        """
        query = 'SELECT * FROM {}'.format(table_name)
        table, col_names = self.execute_query(query)
        self.write_to_file(table, col_names, fname)


    def execute_directly(self, query, fname):
        """Try to execute query directly, without any parsing
        """
        try:
            table, col_names = self.execute_query(query)
            self.write_to_file(table, col_names, fname)
            self.print_table(table)
            return 1
        except:
            return 0
