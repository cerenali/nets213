#! /usr/bin/python2

# input : one gold standard CSV file and one worker CSV file (passed in as
#   command line arguments; see example command)

# output : calculates the performance of each worker, as well as the workers
#   as a whole (by taking the number of labels that match the gold standard and
#   dividing by total number of labels), then prints this to the console,
#   to be copied and pasted into the team_performance.html column chart

# example : `python generate_worker_chart_data.py ../../data/annotator_agreement/gold_standard_annotations.csv ../../data/annotator_agreement/turkers_50_annotations.csv`

# author : a mysterious bumbledinger

import unicodecsv as csv
import sys
from collections import defaultdict

gold_file = csv.DictReader(open(sys.argv[1]))
worker_file = csv.DictReader(open(sys.argv[2]))

# dictionary that maps HIT ID to the respective gold label
gold_pos_labels = {}
gold_neg_labels = {}

# fill gold_labels
for line in gold_file:
  hitId = line['HITId'].encode('UTF-8')
  gold_pos_labels[hitId] = line['positive_gold_label'].encode('UTF-8')
  gold_neg_labels[hitId] = line['negative_gold_label'].encode('UTF-8')

# dictionaries that maps worker ID to a list of [num_pos_correct, num_neg_correct, num_completed]
worker_scores = defaultdict(lambda: [0, 0, 0])

# aggregated over all workers
majority_pos_score = 0
majority_neg_score = 0
total_completed = 0

# fill worker score dictionaries
for line in worker_file:
  hitId = line['HITId'].encode('UTF-8')
  workerId = line['WorkerId'].encode('UTF-8')
  positive = line['Answer.positive_label'].encode('UTF-8')
  negative = line['Answer.negative_label'].encode('UTF-8')

  # increment num_completed
  worker_scores[workerId][2] += 1
  total_completed += 1

  if positive == gold_pos_labels[hitId]:
    worker_scores[workerId][0] += 1
    majority_pos_score += 1

  if negative == gold_neg_labels[hitId]:
    worker_scores[workerId][1] += 1
    majority_neg_score += 1

# calculate actual percentages (both positive and negative) for workers
for worker in worker_scores:
  divisor = worker_scores[worker][2]
  # print 'completed: ' + str(worker_scores[worker][2]) + ' | pos correct: ' + str(worker_scores[worker][0]) + ' | neg correct: ' + str(worker_scores[worker][1])
  worker_scores[worker][0] = round(float(worker_scores[worker][0]) / divisor * 100, 2)
  worker_scores[worker][1] = round(float(worker_scores[worker][1]) / divisor * 100, 2)
  # print '  > scores: ' + str(worker_scores[worker][0]) + ', ' + str(worker_scores[worker][1])

majority_pos_score = round(float(majority_pos_score) / total_completed * 100, 2)
majority_neg_score = round(float(majority_neg_score) / total_completed * 100, 2)

# print output for chart data
print "['Majority', " + str(majority_pos_score) + ", " + str(majority_neg_score) + "],"
for worker in sorted(worker_scores, key=lambda x : worker_scores[x][0], reverse=True):
  # truncate printing of worker ID for brevity + a modicum of privacy
  print "['" + worker[:3] + "', " + str(worker_scores[worker][0]) + ", " + str(worker_scores[worker][1]) + "],"










