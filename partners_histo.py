#!/usr/bin/python

import csv
import argparse

parser = argparse.ArgumentParser(
    description='Parse the H2020 cordis csv file and produce statistics about participants',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input", type=str,
                    default='cordis-h2020projects.csv',
                    help="input file")
parser.add_argument("--output", type=str,
                    default='output.dat',
                    help="input file")
parser.add_argument("--count", type=str,
                    default='',
                    help="count the number of projects of a given participant")
parser.add_argument("--histo", action="store_true",
                    default=False,
                    help="print the histogram of projects by participant")
parser.add_argument("--no_names", action="store_true",
                    default=False,
                    help="do not print the participant names")
parser.add_argument("--no_country", action="store_true",
                    default=False,
                    help="do not distinguish participants based on country")
parser.add_argument("--delimiter", type=str,
                    default=';',
                    help="delimiter")
args = parser.parse_args()

if args.count and args.histo:
    raise Exception("Options --count and --histo are incompatible")

num_rows = 0
participants = dict()
with open(args.input, 'rb') as csvfile:
    cordis = csv.reader(csvfile, delimiter=args.delimiter, quotechar='"')
    for row in cordis:
        num_rows += 1
        name = '{} ({})'.format(row[16], row[17]) \
            if not args.no_country \
            else row[16]
        if name not in participants:
            participants[name] = 0
        participants[name] = participants[name] + 1
        for part,count in zip(row[18].split(';'), row[19].split(';')):
            if len(part) == 0:
               continue
            name = '{} ({})'.format(part, count) \
                if not args.no_country \
                else part
            if name not in participants:
                participants[name] = 0
            participants[name] = participants[name] + 1

if args.count:
    print participants[args.count]

elif args.histo:
    histo_values = [1, 2, 3, 4, 5, 10, 50, 100, 500]
    histo_values_upper = histo_values[1:]
    histo_values_upper.append(num_rows)
    histo = dict()
    for h in histo_values:
        histo[h] = 0
    for part, cnt in sorted(participants.items(), key=lambda x: x[1], reverse=False):
        for lhs, rhs in zip(histo_values, histo_values_upper):
            if lhs <= cnt < rhs:
                histo[lhs] += 1
    with open(args.output, 'wb') as outfile:
        for k, v in sorted(histo.items(), key=lambda x: x[0], reverse=False):
            outfile.write('{} {}\n'.format(k, v))

else:
    print ('total number of projects:     {}\n'
           'total number of participants: {}').format(num_rows, len(participants))
    with open(args.output, 'wb') as outfile:
        for part, cnt in sorted(participants.items(), key=lambda x: x[1], reverse=True):
            if args.no_names:
                outfile.write('{}\n'.format(cnt))
            else:
                outfile.write('{};{}\n'.format(part, cnt))
