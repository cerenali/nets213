#! /usr/bin/python2

# input : one gold standard CSV file and one worker CSV file (passed in as
#   command line arguments; see example command)

# output : calculates the performance of the quality control results (by taking 
#   the number of labels that match the gold standard and dividing by total 
#   number of labels), then prints the result to be copied and pasted into
#   the team chart.

# example : python generate_worker_qc_chart_data.py <gold standard file> <qc file>

# example : python generate_worker_qc_chart_data.py ../../../data/preliminary_analysis/50_tweet_gold_labels.csv ../../../data/full_batch/quality_control_HIT_out.csv

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
from collections import defaultdict

gold_file = csv.DictReader(open(sys.argv[1]))
qc_file = csv.DictReader(open(sys.argv[2]))

# dictionary that maps HIT ID to the respective gold label
gold_pos_labels = {}

# fill gold_labels
for line in gold_file:
  tweet_text = line['Input.text'].encode('UTF-8').replace('\n', ' ')
  gold_pos_labels[tweet_text] = line['positive_gold_label'].encode('UTF-8').replace('_', ' ')

# aggregated over all workers
qc_pos_score = 0
total_completed = 0

# fill worker score dictionaries
for line in qc_file:
  tweet_text = line['Input.text'].encode('UTF-8').replace('\n', ' ')
  positive = line['Answer.positive_label'].encode('UTF-8').replace('_', ' ')

  # filter out tweets that aren't in our sample
  if tweet_text in gold_pos_labels:
    total_completed += 1
    if positive == gold_pos_labels[tweet_text]:
      qc_pos_score += 1

qc_pos_score = round(float(qc_pos_score) / total_completed * 100, 2)

print str(qc_pos_score)