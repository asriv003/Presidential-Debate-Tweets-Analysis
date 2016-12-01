# -*- coding: utf-8 -*-
from __future__ import division
from settings import *
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from nltk.classify import ClassifierI
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from statistics import mode
from nltk.tokenize import word_tokenize
import sys
# from unidecode import unidecode
reload(sys)
sys.setdefaultencoding('utf8')

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


pickled_documents = open("pickled/documents.pickle", "rb")
documents = pickle.load(pickled_documents)
pickled_documents.close()

feat5k = open("pickled/feat5k.pickle", "rb")
word_features = pickle.load(feat5k)
feat5k.close()



def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

pickled_featureset = open("pickled/featureset.pickle", "rb")
featuresets = pickle.load(pickled_featureset)
pickled_featureset.close()
    
# featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)
print len(featuresets)

      
training_set = featuresets[:10000]
testing_set =  featuresets[10000:]


classifier_file = open("pickled/naivebayes5k.pickle","rb")
classifier = pickle.load(classifier_file)
classifier_file.close()
# classifier.show_most_informative_features(15)


classifier_file = open("pickled/MNB5k.pickle","rb")
MNB_classifier = pickle.load(classifier_file)
classifier_file.close()


classifier_file = open("pickled/BernoulliNB5k.pickle","rb")
BernoulliNB_classifier = pickle.load(classifier_file)
classifier_file.close()


classifier_file = open("pickled/Logistic5k.pickle","rb")
LogisticRegression_classifier = pickle.load(classifier_file)
classifier_file.close()

classifier_file = open("pickled/SGDC5k.pickle","rb")
SGDClassifier_classifier = pickle.load(classifier_file)
classifier_file.close()


classifier_file = open("pickled/linearSVC5k.pickle","rb")
LinearSVC_classifier = pickle.load(classifier_file)
classifier_file.close()
# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
# print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


voted_classifier = VoteClassifier(classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

# print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)


print sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!")
print sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10")
print sentiment("george washington watching this debate from heaven")