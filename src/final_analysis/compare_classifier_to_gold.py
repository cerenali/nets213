#! /usr/bin/python2
# Author : John Hewitt : johnhew@seas.upenn.edu
# 
# USAGE:  python2 compare_classifier_to_gold.py <gold_label_tsv> <classifier_label_tsv> > <resuls_summary> 
#

import unicodecsv as csv
import sys

gold_input = csv.reader(open(sys.argv[1]), delimiter='\t')
classifier_input = csv.reader(open(sys.argv[2]), delimiter='\t')


# Total stats
count = 0
correct = 0

# Individual label accuracies
label_to_correct = {'friends':0, 'general_internet_community':0, 'specific_organization':0, 'family':0, 'coworkers':0}
label_to_total = {'friends':0, 'general_internet_community':0, 'specific_organization':0, 'family':0, 'coworkers':0}
int_to_label = {'0':'friends', '1':'family', '2':'coworkers', '3':'general_internet_community', '4':'specific_organization'}

for (gold, classifier) in zip(gold_input, classifier_input):
    gold_label_int = gold[0]
    gold_label_string = int_to_label[gold_label_int]
    classifier_label_int = classifier[0]
    if classifier_label_int == gold_label_int:
        correct += 1
        label_to_correct[gold_label_string] += 1
    count += 1
    label_to_total[gold_label_string] += 1

accuracy =  float(correct) / float(count)
friends_accuracy = float(label_to_correct['friends']) / float(label_to_total['friends'])
family_accuracy = float(label_to_correct['family']) / float(label_to_total['family'])
coworkers_accuracy = float(label_to_correct['coworkers']) / float(label_to_total['coworkers'])
gen_accuracy = float(label_to_correct['general_internet_community']) / float(label_to_total['general_internet_community'])
spec_accuracy = float(label_to_correct['specific_organization']) / float(label_to_total['specific_organization'])


print "Out of %s tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(count, correct, accuracy)
print "Out of %s friends tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(label_to_total['friends'], label_to_correct['friends'], friends_accuracy)
print "Out of %s family tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(label_to_total['family'], label_to_correct['family'], family_accuracy)
print "Out of %s general internet community tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(label_to_total['general_internet_community'], label_to_correct['general_internet_community'], gen_accuracy)
print "Out of %s coworkers tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(label_to_total['coworkers'], label_to_correct['coworkers'], coworkers_accuracy)
print "Out of %s specific organization tweets, the classifier correctly labelled %s. This is an accuracy of %s"%(label_to_total['specific_organization'], label_to_correct['specific_organization'], spec_accuracy)
print "The majority-label baseline is %s"%(float(label_to_correct['friends'])/count)
