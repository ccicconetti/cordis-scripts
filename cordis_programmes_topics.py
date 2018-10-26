#!/usr/bin/python
"""Filter the CORDIS csv file to file all programmes and topics"""

import os.path
import csv
import argparse

parser = argparse.ArgumentParser(
    description="Filter the CORDIS csv file to file all programmes and topics",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--input",
    type=str,
    default="h2020projects.csv",
    help="name of the CSV file where to read the project data from")
parser.add_argument(
    "--output_programmes",
    type=str,
    default="programmes.txt",
    help="name of the file where to save the programmes")
parser.add_argument(
    "--output_topics",
    type=str,
    default="topics.txt",
    help="name of the file where to save the topics")
parser.add_argument(
    "--overwrite",
    action="store_true",
    default=False,
    help="overwrite output file if existing")
args = parser.parse_args()

programmes = set()
topics = set()

with open(args.input, 'rb') as csvfile:
    cordis = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in cordis:
        programmes.add(row[4])
        topics.add(row[5])

if not args.overwrite and os.path.exists(args.output_programmes):
    raise Exception("cannot overwrite output file " + args.output_programmes)
if not args.overwrite and os.path.exists(args.output_topics):
    raise Exception("cannot overwrite output file " + args.output_topics)

with open(args.output_programmes, 'w') as programmefile:
    for x in sorted(programmes):
        for y in x.split(';'):
            programmefile.write(y + '\n')

with open(args.output_topics, 'w') as topicsfile:
    for x in sorted(topics):
        topicsfile.write(x + '\n')

