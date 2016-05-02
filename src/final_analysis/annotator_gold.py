#! /usr/bin/python2
#
# Takes 3 CSVs with 'expert' annotations of some tweets. 
# Determines the majority label and outputs this as the majority label or asks for help if
# There's no majority
#
# Author : John Hewitt : johnhew@seas.upenn.edu

import unicodecsv as csv
import sys
import collections

# Dictionaries to store the annotators' answers
results = {}

# HIT ID to Tweet
ID_to_tweet = {}

# Files in which the annotators' labels are stored
one_file = csv.DictReader(open(sys.argv[1]))
two_file = csv.DictReader(open(sys.argv[2]))
three_file = csv.DictReader(open(sys.argv[3]))



def add_results(annotator_file):
    for line in annotator_file:
        tweet = line['Input.text']
        positive = line['positive_label']
        negative = line['negative_label']

        if tweet not in results:
            results[tweet] = collections.defaultdict(int)
        results[tweet][positive] += 1
        results[tweet][negative] -= 1

        ID_to_tweet[tweet] = tweet




# Iterate through each of the annotators, populating their result dictionaries
add_results(one_file)
add_results(two_file)
add_results(three_file)


# Results will be written to stdout
writer = csv.writer(sys.stdout)
writer.writerow(['HITId', 'Input.text', 'Answer.positive_label', 'Answer.negative_label'])

# Now, iterate through the HIT IDs, spitting out the majority label for each
for ID in ID_to_tweet:
    tweet = ID_to_tweet[ID]
    label_dict = results[ID]
    sorted_labels = [(x, label_dict[x]) for x in sorted(label_dict.keys(), key=lambda x : label_dict[x], reverse=True)]

    positive_label = sorted_labels[0][0]
    negative_label = sorted_labels[-1][0]
    writer.writerow([ID, tweet, positive_label, negative_label])
