#! /usr/bin/python2
# Author : John Hewitt : johnhew@seas.upenn.edu
#
# Takes tweet-labeling HIT output on stdin
# Prints tweet with majority label and all creative labels on stdout

import unicodecsv as csv
import sys
import collections


# Class encapsualating all data associated with a single tweet
class Tweet:

    def __init__(self, tweet, url):
        self.tweet = tweet
        self.url = url
        self.label_counts = collections.defaultdict(int)
        self.creative_labels = []

    def add_creative(self, label):
        self.creative_labels.append(label)

    def add_pos(self, label):
        self.label_counts[label] += 1

    def add_neg(self, label):
        self.label_counts[label] -= 1

    def __eq__(self, other):
        return self.text == other.text

    def __ne__(self, other):
        return self.text != other.text

    def __hash__(self):
        return self.tweet.__hash__()



# Iterate through tweets, aggregating data about each tweet
tweetdict = {}
for line in csv.DictReader(sys.stdin):
    tweet_text = line['Input.text'].replace('\n', ' ')
    url = line['Input.url']
    pos_label = line['Answer.positive_label']
    neg_label = line['Answer.negative_label']
    creative_label = line['Answer.creative_label']

    tweet = None
    if tweet_text not in tweetdict:
        print 'new tweet'
        print '+++', tweet_text
        tweet = Tweet(tweet_text, url)
        tweetdict[tweet_text] = tweet
    else:
        tweet = tweetdict[tweet_text]

    tweet.add_creative(creative_label)
    tweet.add_neg(neg_label)
    tweet.add_pos(pos_label)



writer = csv.DictWriter(open('aggregation1_out.csv', 'w'), ['text', 'link', 'label1', 'label2', 'friends', 'family', 'coworkers', 'general_internet_community', 'specific_internet_community', 'creative_label_1', 'creative_label_2', 'creative_label_3', 'creative_label_4', 'creative_label_5', 'creative_label_6', 'creative_label_7'])
writer.writeheader()
for tweet_text in tweetdict:
    tweet = tweetdict[tweet_text]
    sorted_tweets = [(x, tweet.label_counts[x]) for x in sorted(tweet.label_counts.keys(), key=lambda x : tweet.label_counts[x], reverse=True)]

    print tweet.creative_labels

    writer.writerow({
        'tweet':tweet.tweet,
        'link':tweet.url,
        'label1': sorted_tweets[0][0],
        'label2': sorted_tweets[1][0],
        'friends': tweet.label_counts['friends'],
        'family': tweet.label_counts['family'],
        'coworkers': tweet.label_counts['coworkers'],
        'general_internet_community': tweet.label_counts['general_internet_community'],
        'specific_internet_community': tweet.label_counts['specific_internet_community'],
        'creative_label_1': tweet.creative_labels[0],
        'creative_label_2': tweet.creative_labels[1],
        'creative_label_3': tweet.creative_labels[2],
        'creative_label_4': tweet.creative_labels[3],
        'creative_label_5': tweet.creative_labels[4],
        'creative_label_6': tweet.creative_labels[5],
        'creative_label_7': tweet.creative_labels[6]})

