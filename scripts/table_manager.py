#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shutil
import csv
import re
import sys


FUNCTIONS = ['COUNT', 'AVG', 'SUM', 'MIN', 'MAX']


class TableManager(object):

    def __init__(self):
        pass

    def write_func_output(self, out_file, func, col_name, output):
        """Write function output to file
        """
        with open(out_file, 'w') as out_f:
            out_f.write('Function: {}\n'.format(func))
            out_f.write('  Column: {}\n'.format(col_name))
            out_f.write('-----------------\n')
            out_f.write('  OUTPUT: {}'.format(output))


    def print_func_output(self, func, col_name, output):
        """Print function output to console
        """
        print('Function: {}'.format(func))
        print('  Column: {}'.format(col_name))
        print('-----------------')
        print('  OUTPUT: {}'.format(output))


    def write_tuples_file(self, tuples_dict, tuples_file):
        """Write tuples to file
        """
        with open(tuples_file, 'w') as tuples_f:
            writer = csv.writer(tuples_f, delimiter='\t')
            writer.writerow([elem for elem in tuples_dict['header']])
            for tpl in tuples_dict['tuples']:
                writer.writerow([elem for elem in tpl])


    def extract_tuples(self, constraints, in_file, tmp_file):
        """Extract tuple if value of the feature in the interval
        """
        with open(in_file, 'r') as in_f:
            reader = csv.reader(in_f, delimiter='\t')
            header = next(reader)
            with open(tmp_file, 'w') as tmp_f:
                writer = csv.writer(tmp_f, delimiter='\t')
                writer.writerow(header)

                for line in reader:
                    constraint_violated = False

                    for constraint in constraints:
                        index = header.index(constraint['feature'])

                        if float(line[index]) not in range(*constraint['interval']):
                            constraint_violated = True
                            break

                    if not constraint_violated:
                        writer.writerow(line)


    def execute_instruction(self, instr, func, col_names, tmp_file, out_file):
        """Execute instruction and function
        """
        if not func:
            if '*' in col_names:
                print('No function, all columns')
                shutil.move(tmp_file, out_file)
                return
            else:
                print('No function, specific columns')
                with open(tmp_file, 'r') as tmp_f:
                    reader = csv.reader(tmp_f, delimiter='\t')
                    header = next(reader)

                    indexes = []
                    for col_name in col_names:
                        indexes.append(header.index(col_name))

                    with open(out_file, 'w') as out_f:
                        writer = csv.writer(out_f, delimiter='\t')
                        writer.writerow(col_names)
                        for line in reader:
                            writer.writerow(line[index] for index in indexes)
                return

        col_name = col_names[0]
        values = []
        with open(tmp_file, 'r') as tmp_f:
            reader = csv.reader(tmp_f, delimiter='\t')
            header = next(reader)

            if col_name == '*':
                col_no = 0
            else:
                col_no = header.index(col_name)
            for line in reader:
                values.append(line[col_no])

        try:
            if func == FUNCTIONS[0]:
                output = len(values)

            values = [float(value) for value in values]
            if func == FUNCTIONS[1]:
                output = sum(values)/float(len(values))

            elif func == FUNCTIONS[2]:
                output = sum(values)

            elif func == FUNCTIONS[3]:
                output = min(values)

            elif func == FUNCTIONS[4]:
                output = max(values)

            output = round(output, 2)
        except ValueError:
            print('Error while executing function, possibly caused by'
                  + ' lack of tuples fulfilling constraints. Exiting.')
            sys.exit(1)

        self.print_func_output(func, col_name, output)
        self.write_func_output(out_file, func, col_name, output)

        return
