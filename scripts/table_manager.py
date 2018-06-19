#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shutil
import csv
import re
import sys


INSTRUCTIONS = ['SELECT']
FUNCTIONS = ['COUNT', 'AVG', 'SUM', 'MIN', 'MAX']


class TableManager(object):

    def __init__(self):
        pass

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
        #TODO: Finish implementation of this function

        if not func:
            if '*' in col_names:
                print('INSIDE IF')
                shutil.move(tmp_file, out_file)
                return
            else:
                print('INSIDE ELSE')
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

        if func == FUNCTIONS[0]:
            pass
        elif func == FUNCTIONS[1]:
            pass
        elif func == FUNCTIONS[2]:
            pass
        elif func == FUNCTIONS[3]:
            pass
        else:
            pass
        print('OUTSIDE EVERYTHING')

        """values_list = []
        with open(tmp_file, 'r') as tmp_f:
            reader = csv.reader(in_f, delimiter='\t')
            header = next(reader)

            col_no = header.index(col_names[0])
            for line in tmp_f:
                values_list.append(line[column_no])

            if func == FUNCTIONS[0]:
                out_value = sum(1 for line in f)

            elif func == FUNCTIONS[1]:
                sum_value = 0
                len_value = 0
                for line in f:
                    sum_value = sum(sum_value, line[column_no])
                    len_value += 1
                out_value = sum_value / float(len_value)

            elif func == FUNCTIONS[2]:
                out_value = sum(line[column_no] for line in f)

            elif func == FUNCTIONS[3]:
                pass

            elif func == FUNCTIONS[4]:
                pass"""
