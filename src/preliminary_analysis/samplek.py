#! /usr/bin/python2
#
# Takes a CSV with results, de-dupes on HIT_ID, and writes the ID and the input text to a new CSV.
#
# Author : John Hewitt : johnhew@seas.upenn.edu

import unicodecsv as csv
import sys

hdict = {}
for line in csv.DictReader(sys.stdin):
    hdict[line['HITId']] = line['Input.text'].replace('\n', ' ')

writer = csv.writer(sys.stdout)
writer.writerow(['HITId', 'Input.text'])
for count, i in enumerate(hdict):
    if count == 50:
        break
    writer.writerow([i, hdict[i]])





