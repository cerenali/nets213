#! /usr/bin/python2
#
# Takes a CSV with results, de-dupes on HIT_ID, and writes the ID and the input text to a new CSV.
#
# Author : John Hewitt : johnhew@seas.upenn.edu

import unicodecsv as csv
import sys

hdict = {}
for line in csv.DictReader(open(sys.argv[1])):
    hdict[line['HITId']] = line['Input.text'].replace('\n', ' ')

writer = csv.writer(sys.stdout)
writer.writerow(['HITId', 'Input.text'])
for line in csv.reader(sys.stdin):
    if line[0] in hdict:
        writer.writerow(line)
