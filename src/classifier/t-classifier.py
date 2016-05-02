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

#this is the main function you care about; pack all the cleverest features you can think of into here.
def get_features(X) : 
	features = []
    
        #neighbors_sets = get_vectors()
	for x in X : 
		f = {}

                # Unigram Features
                for w in [word.strip(string.punctuation) for word in x.split()] :
                    f[w] = 1.0

                # Bigram Features
                prior = []
                for w in [word.strip(string.punctuation) for word in x.split()] :
                    if len(prior) == 2:
                        prior.pop(0)
                    prior.append(w)
                    if len(prior) == 2:
                        f[' '.join(prior)] = 1

                # Trigram Features
                prior = []
                for w in [word.strip(string.punctuation) for word in x.split()] :
                    if len(prior) == 3:
                        prior.pop(0)
                    prior.append(w)
                    if len(prior) == 3:
                        f[' '.join(prior)] = 1

                # @ Sign Binary Feature
                if "@" in x:
                    f["BINARY: @ sign present"] = 1

                # Ternary length feature"
                if len(x) <47:
                    f['TERNARY: short'] = 1
                if len(x) > 47 and len(x) < 95:
                    f['TERNARY: medium'] = 1
                if len(x) > 94:
                    f['TERNARY: long'] = 1

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

def get_matricies_for_unlabelled(text, dv, le) : 
	X = get_features([text])
	return dv.transform(X), dv, le

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
#	for i,w in features:
#	  print '%s\t%s'%(feature_names[i], w)

def predict_unlabelled(clf, X, outfile) : 
	num_articles = X.shape[0]
	for i,x in enumerate(X) : 
		outfile.write('%d\n'%clf.predict(x)[0])

def get_classifier(filename):
    y, X, texts, dv, le = get_matricies(raw_data)
    return train_classifier(X,y)

if __name__ == '__main__' : 

	#The program expects 2 arguments, a file containing training data and a file containing unlabelled data. 
	#If it does not get two arguments, print instructions and exit
	if len(sys.argv) < 3 : print "Usage: python classifier.py TRAINING_DATA UNLABELLED_DATA [n]"; exit(0)
	#Optionally, specify a number of lines of unlabelled data to predict
	n = None if len(sys.argv) < 4 else int(sys.argv[3])
	
	#Load the training data and then unseen data
	sys.stderr.write("Reading raw data\n")
	training_data = get_data(sys.argv[1])
	
	sys.stderr.write("Loading training data\n")
	#Convert training data into a label vector y and a feature matrix X
	y, X, texts, dv, le = get_matricies(training_data)

	sys.stderr.write("Training classifier\n")
	#Train your classifer on all the data you have
	clf = train_classifier(X,y) 
	
	sys.stderr.write("Loading unlabelled data\n")
	
	outfile = open("classifier_predictions.txt", 'w')
	with open(sys.argv[2]) as f : 
		
		for i,text in enumerate(f) :
			if i%10000 == 0 : sys.stderr.write("Predicting article # %d\n"%(i))
			if n and (i > n) : break 
			x, dv, le = get_matricies_for_unlabelled(text, dv, le)
			predict_unlabelled(clf, x, outfile)
	
        
        
    	get_top_features(X, y, dv)
        
    	#get_misclassified_examples(y, X, texts)

