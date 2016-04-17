#!/bin/python
# Author : NETS 213 Staff, John Hewitt johnhew@seas.upenn.edu
#
# Learns a classifier that assigns social sphere labels to tweets
#



import os
import sys
import string
import random
import operator
import csv
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.externals.six import StringIO  


#read in raw data from file and return a list of (label, article) tuples
def get_data(filename): 
	data = [line.strip().split('\t') for line in open(filename).readlines()]
	random.shuffle(data)
	return data

# Offer up the top 100 most distributionally similar words to the word 'gunman' 
# and 'shooting' and 'bullet' to add some binary features.
# Computed using my wrapper of Google's word2vec and their own vector set.
# Returns 5-tuple of arrays of string neighbors
#def get_vectors():
#    vecs = {}
#    gunman_neighbors = ['lone_gunman']
#    return (gunman_neighbors,)

#this is the main function you care about; pack all the cleverest features you can think of into here.
def get_features(X) : 
	features = []
    
        #neighbors_sets = get_vectors()
	for x in X : 
		f = {}
                for w in [word.strip(string.punctuation) for word in x.split()] :
                    f[w] = 1.0
                # Gunman distributional similarity neighbors
                #for neighbors in neighbors_sets:
                #    for neighbor in neighbors:
                #        if neighbor in x:
                #            f[neighbor + '_gunman_vector_sim'] = 1.0

                # unigram features
                    
                # bigram features that include the words 'gun' or 'gunman' or 'shooting'
                #prior_word = ''
                #for w in [word.strip(string.punctuation) for word in x.split()] :
                #    if prior_word in ['gun', 'gunman', 'shooting'] or \
                #            w in ['gun', 'gunman', 'shooting']:
                #                f[w+'_'+prior_word] = 1.0
                #    prior_word = w
            
		features.append(f)
	return features

#vectorize feature dictionaries and return feature and label matricies
def get_matricies(data, typ="unigram") : 
	dv = DictVectorizer(sparse=True) 
	le = LabelEncoder()
	y = [d[0] for d in data]
	texts = [d[1] for d in data]
        X = get_features(texts)
	# Here we are returning 5 things, the label vector y and feature matrix X, 
        # but also the texts from which the features were extracted and the 
	# objects that were used to encode them. These will come in handy for your analysis, 
        # but you can ignore them for the initial parts of the assignment
	return le.fit_transform(y), dv.fit_transform(X), texts, dv, le

#train and multinomial naive bayes classifier
def train_classifier(X, y):
	clf = LogisticRegression()
	clf.fit(X,y)
	return clf 

#test the classifier
def test_classifier(clf, X, y):
	return clf.score(X,y)

#cross validation	
def cross_validate(X, y, dv=None, typ="unigram", numfolds=5,):
	test_accs = []
	split = 1.0 / numfolds
	for i in range(numfolds):
		x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=i)
		if typ == "tree" :
			clf = train_dtree_classifier(x_train, y_train)
		else :
			clf = train_classifier(x_train, y_train)
		test_acc = test_classifier(clf, x_test, y_test)
		test_accs.append(test_acc)
		print 'Fold %d : %.05f'%(i,test_acc)
	test_average = float(sum(test_accs))/ numfolds
	if typ == "tree" :
		with open("output.dot", 'w') as f:
			f = export_graphviz(clf, out_file=f, feature_names=dv.get_feature_names(), class_names=['Non Gun Related','Gun Related'])
		create_graph("decision-tree.png")
	print 'Test Average : %.05f'%(test_average)
	return test_average


#train and multinomial naive bayes classifier
def get_top_features(X, y, dv):
	clf = train_classifier(X, y)
	#the DictVectorizer object remembers which column number corresponds to which feature, and return the feature names in the correct order
	feature_names = dv.get_feature_names() 

	#The below code will get the weights from the classifier, and print out the weights of the features you are interested in
	features = [] #this will be a list of (feature_idx, weight) tuples
	for i,w in enumerate(clf.coef_[0]): 
		features.append((i,w))
	#Sort the list by values, with the largest ones first
	features = sorted(features, key=lambda e: e[1], reverse=True)

        #Print out the feature names and thier weights
	for i,w in features:
	  print '%s\t%s'%(feature_names[i], w)

def get_classifier(filename):
    y, X, texts, dv, le = get_matricies(raw_data)
    return train_classifier(X,y)

if __name__ == '__main__' : 
	raw_data = get_data(sys.argv[1])
	
################ Statistical Classification ################
	print '\nStatistical classification'
	y, X, texts, dv, le = get_matricies(raw_data)
	cross_validate(X,y)

    	get_top_features(X, y, dv)
    	#get_misclassified_examples(y, X, texts)

