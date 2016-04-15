#! /usr/bin/python2
# Author : John Hewitt : johnhew@seas.upenn.edu
#
# Takes quality-controlled tweet lable output of the CSV form on STDIN
#           tweet,link,final_label,creative_label_1,creative_label_2,\
#           creative_label_3,creative label 4,creative label 5,creative label 6,creative label
# 
# Outputs, in a constructed folder called "training", one training file per class in our multi-class 
# classification task. Each file is of the form:
#       Name: <class_name>.txt
#               <0/1>\t<tweet_text>
#
# Thus, each file will be used to train a binary classifier on individual labels.

import unicodecsv as csv
import sys
import os

# Create and move into the directory to store the training files
os.mkdir('training')
os.chdir('training')


# Create a CSV writer for each class
friends_writer = csv.writer(open('friends_train', 'w'), delimiter='\t')
family_writer = csv.writer(open('family_train', 'w'), delimiter='\t')
coworkers_writer = csv.writer(open('coworkers_train', 'w'), delimiter='\t')
general_writer = csv.writer(open('general_train', 'w'), delimiter='\t')
specific_writer = csv.writer(open('specific_train', 'w'), delimiter='\t')

# Map the name of the label to the writer that will write the training file for the 
# corresponding classifier
label_to_writer = {'friends':friends_writer, 'family':family_writer, 'coworkers':coworkers_writer, 
        'general_internet_community':general_writer, 'specific_internet_community':specific_writer}
        

# Iterate through the labelled tweets, writing each tweet to all of the training files,
# Labelling as 0 or 1 if an instance of each label
for line in csv.DictReader(sys.stdin):
    label = line['final_label']
    tweet_text = line['tweet'].replace('\n', ' ')
    label_int = label_to_writer[label]
    for key in label_to_writer:
        if key == label:
            label_to_writer[key].writerow(['1', tweet_text])
        else:
            label_to_writer[key].writerow(['0', tweet_text])



