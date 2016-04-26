#! /usr/bin/python2

# input : one gold standard CSV file and one contributor CSV file

# output : calculates the performance of the contributor
#   (by taking the number of labels that match the gold standard and
#   dividing by total number of labels) and prints this to the console,
#   to be copied and pasted into the team_performance.html column chart

# example : `python generate_team_chart_data.py ../../data/annotator_agreement/gold_standard_annotations.csv ../../data/annotator_agreement/alice_annotations.csv`

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
import collections

gold_file = csv.DictReader(open(sys.argv[1]))
contributor_file = csv.DictReader(open(sys.argv[2]))

# dictionary that maps HIT id to the respective gold label
gold_pos_labels = {}
gold_neg_labels = {}

# fill gold_labels
for line in gold_file:
  hitId = line['HITId'].encode('UTF-8')
  gold_pos_labels[hitId] = line['positive_gold_label'].encode('UTF-8')
  gold_neg_labels[hitId] = line['negative_gold_label'].encode('UTF-8')

def calculate_percentage_matched(annotator_file):
  pos_matched = 0
  neg_matched = 0
  for line in annotator_file:
    hitId = line['HITId'].encode('UTF-8')
    positive = line['positive_label'].encode('UTF-8')
    negative = line['negative_label'].encode('UTF-8')

    if positive == gold_pos_labels[hitId]:
      pos_matched += 1

    if negative == gold_neg_labels[hitId]:
      neg_matched += 1

  return (float(pos_matched) / len(gold_pos_labels) * 100, float(neg_matched) / len(gold_neg_labels) * 100)


pos_correct, neg_correct = calculate_percentage_matched(contributor_file)

# fill in the name by hand 
print "['', " + str(pos_correct) + ", " + str(neg_correct) + "],"