#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shutil
import csv


INSTR = ['select', 'count']


def write_tuples_file(tuples_dict, tuples_file):
    """Write tuples to file
    """
    with open(tuples_file, 'w') as tuples_f:
        writer = csv.writer(tuples_f, delimiter='\t')
        writer.writerow([elem for elem in tuples_dict['header']])
        for tpl in tuples_dict['tuples']:
            writer.writerow([elem for elem in tpl])


def extract_tuples(feature, interval, table_file, tuples_file):
    """Extract tuple if value of the feature in the interval
    """
    tuples = []
    with open(table_file, 'r') as table_f:
        header = tuple(table_f.readline().strip('\n').split('\t'))
        index = header.index(feature)
        for line in table_f:
            tpl = tuple(line.strip('\n').split('\t'))
            feature_val = float(tpl[index])
            if feature_val in interval:
                tuples.append(tpl)
    tuples_dict = {'header': header, 'tuples': tuples}
    #print(json.dumps(tuples_dict, indent=4, ensure_ascii=False))
    write_tuples_file(tuples_dict, tuples_file)


def execute_instruction(instr, tuples_file, output_file):
    """Execute instruction
    """
    if instr == INSTR[0]:
        shutil.move(tuples_file, output_file)
    elif instr == INSTR[1]:
        with open(tuples_file, 'r') as tuples_f:
            num_lines = sum(1 for line in tuples_f)-1
        with open(output_file, 'w') as output_f:
            output_f.write('{}'.format(num_lines))

