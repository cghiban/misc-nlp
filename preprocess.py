# -*- coding: utf-8 -*-
"""
Preprocessor and analyzer for infinitives
Created on Wed Apr 13 18:13:21 2011

@author: vene
"""

from sklearn.feature_extraction.text import CharNGramAnalyzer, CountVectorizer
from sklearn.preprocessing import Binarizer
from sklearn.pipeline import Pipeline
from sklearn import naive_bayes
import codecs

import numpy as np

class SimplePreprocessor(object):
    def preprocess(self, unicode_text):
        return unicode(unicode_text.strip().lower() + self.suffix)
        
    def __init__(self, suffix=''):
        self.suffix = suffix


def get_clf(n=3, binarize=True, clf=None):
    steps = [('vectorizer', CountVectorizer(CharNGramAnalyzer(min_n=1, max_n=n,
                                          preprocessor=SimplePreprocessor())))]
    if binarize:
        steps.append(('binarizer', Binarizer(copy=False)))
        if not clf:
            clf = naive_bayes.BernoulliNB()
    elif not clf:
        clf = naive_bayes.MultinomialNB()
    steps.append(('clf', clf))
    return Pipeline(steps)


def preprocess_data(X, n=3, suffix='', binarize=True, return_vect=False):
    cv = CountVectorizer(CharNGramAnalyzer(min_n=1, max_n=n,
                                           preprocessor=SimplePreprocessor(
                                           suffix)))
    X = cv.fit_transform(X)
    if binarize:
        X = Binarizer(copy=False).transform(X)
    
    if return_vect:
        return X, cv
    else:
        return X


def load_data(filename='inf-ta-labeled.txt', labels=True):
    infinitives, y = [], []
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if labels:
                inf, label = line.split()
            else:
                inf = line
            infinitives.append(inf)
            if labels:
                y.append(int(label))
    infinitives, y = np.array(infinitives), np.array(y, dtype=np.int)
    if labels:
        return infinitives, y
    else:
        return infinitives
