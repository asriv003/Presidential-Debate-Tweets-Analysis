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
from nltk.corpus import stopwords
import sys
# from unidecode import unidecode
reload(sys)
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()

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

short_pos = open("positive.txt","r").read()
short_neg = open("negative.txt","r").read()
# For decoding issue with UTF-8 and ASCII
pos = short_pos.decode('utf8')
neg = short_neg.decode('utf8')

documents = []
complete_list = []
# Adjective - 'J' Verb - 'VB'
part_of_speech_tags = ['J', 'V']
stop_word = set(stopwords.words("english"))
print stop_word
for line in pos.split('\n'):
    documents.append((line, "pos"))
    pos_words = word_tokenize(line)
    words = nltk.pos_tag(pos_words)
    for word in words:
        if word not in stop_word:
            if word[1][0] in part_of_speech_tags:
                complete_list.append(word[0].lower())


for line in neg.split('\n'):
    documents.append((line, "neg"))
    neg_words = word_tokenize(line)
    words = nltk.pos_tag(neg_words)
    for word in words:
        if word not in stop_word:
            if word[1][0] in part_of_speech_tags:
                complete_list.append(word[0].lower())

save_documents = open("new_pickled/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

print len(complete_list)

complete_list = nltk.FreqDist(complete_list)

word_features = list(complete_list.keys())[:5000]

save_word_features = open("new_pickled/feat5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features
    
featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)

featureset_pickle = open("new_pickled/featureset.pickle","wb")
pickle.dump(featuresets, featureset_pickle)
featureset_pickle.close()

print len(featuresets)
training_set = featuresets[:10000]
testing_set =  featuresets[10000:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

# Pickling
save_classifier = open("new_pickled/naivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

# Pickling
save_classifier = open("new_pickled/MNB5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

# Pickling
save_classifier = open("new_pickled/BernoulliNB5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

# Pickling
save_classifier = open("new_pickled/Logistic5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

# Pickling
save_classifier = open("new_pickled/SGDC5k.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

# Pickling
save_classifier = open("new_pickled/linearSVC5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
# print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)


print sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!")
print sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10")
print sentiment("george washington watching this from heaven")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           