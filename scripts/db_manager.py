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
        return db_list


    def write_to_file(self, db_list, fname):
        """Write to file
        """
        with open(fname,'w') as f:
            tsv_f = csv.writer(f, delimiter='\t')
            for db_tuple in db_list:
                tsv_f.writerow(db_tuple)


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
        table = self.execute_query(query)
        self.write_to_file(table, fname)


    def execute_directly(self, query, fname):
        """Try to execute query directly, without any parsing
        """
        try:
            table = self.execute_query(query)
            self.write_to_file(table, fname)
            self.print_table(table)
            return 1
        except:
            return 0
