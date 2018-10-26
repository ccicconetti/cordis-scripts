#!/usr/bin/python
"""Filter the CORDIS csv file based on the topic field"""

import os.path
import csv
import argparse

parser = argparse.ArgumentParser(
    description="Extract from the CORDIS csv file the projects with a topic from a list",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--topics_file",
    type=str,
    default="topics.txt",
    help="name of the file containing the topics, one per line")
parser.add_argument(
    "--input",
    type=str,
    default="h2020projects.csv",
    help="name of the CSV file where to read the project data from")
parser.add_argument(
    "--output",
    type=str,
    default="output.csv",
    help="name of the file where to save the result, using CSV")
parser.add_argument(
    "--overwrite",
    action="store_true",
    default=False,
    help="overwrite output file if existing")
args = parser.parse_args()

interests = dict()
with open(args.topics_file, 'r') as interestsfile:
    for line in interestsfile:
        interest = line.rstrip()
        if not interest in interests:
            interests[interest] = 0

if not args.overwrite and os.path.exists(args.output):
    raise Exception("cannot overwrite output file " + args.output)

with open(args.input, 'rb') as csvinputfile, open(args.output, 'w') as csvoutputfile:
    cordis = csv.reader(csvinputfile, delimiter=';', quotechar='"')
    out = csv.writer(csvoutputfile)
    for row in cordis:
        if row[5] in interests.keys():
            interests[row[5]] = interests[row[5]] + 1
            out.writerow(row)

for k,v in interests.items():
    print '{} -> {}'.format(k, v)
