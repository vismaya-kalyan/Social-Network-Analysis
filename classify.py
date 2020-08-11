"""
Classify data.
"""

# Load the Pandas libraries with alias 'pd'
import pandas as pd
import numpy as np
# regex to remove punctuations.
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import preprocessor as p
import json
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.MENTION, p.OPT.RESERVED)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

import math
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score


def preprocess(user_df):
    
    punctuations = '!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    regex = re.compile('[%s]' % re.escape(punctuations))
    regexb=re.compile('b[\'\"]')


    arr= []
    for index, tweet in user_df.iterrows():                
        twe = p.clean(tweet['text'])         # remove urls, reserved, emoji, smiley, mention
        twe = twe.lower()          # lower
        twe = regexb.sub('', twe)  # remove quotes  
        twe = regex.sub('', twe)   # remove punctuations
        arr.append(twe)

    user_df.insert(3, "pre_processed", arr) 

    return user_df


def show(user_df):
    # We can use the TfidfVectorizer to find ngrams for us
    vect = TfidfVectorizer(ngram_range=(2,5), stop_words='english')

    summaries = "".join(user_df['text'])
    ngrams_summaries = vect.build_analyzer()(summaries)
    # print(user_df)
    print("\n",Counter(ngrams_summaries).most_common(20))


def get_true_labels(tweets):
    """Return a *numpy array* of ints for the true sentiment labels of each file.
    1 means positive, 0 means negative. Use the name of the file to determine
    the true label.
    Params:
        file_names....a list of .txt file paths, e.g., data/train/pos/10057_9.txt
    Returns:
        a numpy array of 1 or 0 values corresponding to each element
        of file_names, where 1 indicates a positive review, and 0
        indicates a negative review.
    """
    return np.array([1 if 'joerogan' in f else 0 for f in tweets['author']])


# Creates a LogsticRegression object.
def get_clf(c=1, penalty='l2'):
    return LogisticRegression(random_state=42, C=c, penalty=penalty,solver='lbfgs')


def do_cross_validation(X, labels, n_folds=5, c=1, penalty='l2', verbose=False):
    """
    Perform n-fold cross validation, calling get_clf() to train n
    different classifiers. Use sklearn's KFold class: http://goo.gl/wmyFhi
    Be sure not to shuffle the data, otherwise your output will differ.
    Params:
        X.........a csr_matrix of feature vectors
        y.........the true labels of each document
        n_folds...the number of folds of cross-validation to do
        verbose...If true, report the testing accuracy for each fold.
    Return:
        the average testing accuracy across all folds.
    """
    cv = KFold(n_splits=n_folds, shuffle=True)
    accuracies = []
    train_accuracies = []
    my_list = []
    for foldi, (train, test) in enumerate(cv.split(X)):
        clf = get_clf(c=c, penalty=penalty)
        clf.fit(X[train], labels[train])
        train_accuracies.append(accuracy_score(clf.predict(X[train]), labels[train]))
        pred = clf.predict(X[test])
        acc = accuracy_score(pred, labels[test])
        accuracies.append(acc)
        if verbose:
            print('fold %d accuracy=%.4g' % (foldi, acc))
            my_list.append('fold %d accuracy=%.4g' % (foldi, acc))
    return my_list, (np.mean(accuracies),
            np.std(accuracies) / math.sqrt(n_folds),
            np.mean(train_accuracies),
            np.std(train_accuracies) / math.sqrt(n_folds))
    

def print_results(results):
    print('test accuracy=%.4f (%.2f) train accuracy=%.4f (%.2f)' % 
           results)
    

""" 
    Read data from file 'filename.csv'
    (in the same directory that your python process is based)
    Control delimiters, rows, column names with read_csv (see later)
"""
def main():
    screen_names = ["jordanbpeterson", "joerogan"]
    jordanbpeterson_df = pd.read_csv("jordanbpeterson_tweets.csv")
    jordanbpeterson_df["author"] = "jordanbpeterson"
    joerogan_df = pd.read_csv("joerogan_tweets.csv")
    joerogan_df["author"] = "joerogan"
    

    jordanbpeterson_df = preprocess(jordanbpeterson_df)
    joerogan_df = preprocess(joerogan_df)

    show(jordanbpeterson_df)
    show(joerogan_df)

    tweets = pd.concat([jordanbpeterson_df, joerogan_df], axis=0)
    print("shape of total data",tweets.shape)

    b=tweets.iloc[:,3].astype(str)

    tfv = TfidfVectorizer(ngram_range=(2,4), max_features=2000)
    X = tfv.fit_transform(b).todense()
    print(X.shape)

    labels = get_true_labels(tweets)
    print('first 3 and last 3 labels are: %s' % str(labels[[1,2,3,-3,-2,-1]]))

    
    my_list, results = do_cross_validation(X, labels, verbose=True)
    print_results(results)

    # Writing output to file
    summary = open('classify.txt', 'w')  # Create file to write summary

    summary.write('\nNumber of instance belonging to jordanbpeterson '+str(jordanbpeterson_df.shape))
    summary.write('\nNumber of instance belonging to joerogan '+str(joerogan_df.shape)) 
    for i in my_list: 
        summary.write('\n'+ str(i))   
    summary.write('\nResults:\nThe data from both the users are combined, preprocessed, shufield.\n' )
    summary.write('A logistic regression is used to predict which tweet belongs to which user\n')
    summary.write('test accuracy=%.4f (%.2f) train accuracy=%.4f (%.2f)' % results)
    summary.close() 


if __name__ == "__main__":
    main()

    
