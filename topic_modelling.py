# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 10:11:46 2016

@author: Vivek
"""

import logging
from config import DATA_DIR
book_data_dir = DATA_DIR +  'book_data.json'
author_data_dir = DATA_DIR + 'author_data.json'
from exp import load_dictionary
from utility import print_log, get_name
from utility import clean_html
import glob
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy
import matplotlib.pyplot as plt


def print_top_words(model, feature_names, n_top_words, book_data = None):
    for topic_idx, topic in enumerate(model.components_):
        print_log("Topic #%d:" % topic_idx)
        print_log(", ".join([get_name(feature_names[i])
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def load_user_data(folder_path, book_id2attr = None):
    '''
    Returns:
        dataset = list of docs. Each doc is a string.
        vocabulary = set of unique words
    '''
    all_user_files = glob.glob(folder_path +'user_*.json')
    dataset = []
    for fpath in all_user_files:
        d = load_dictionary(fpath)
        books = d.values()[0]['books'].keys()
        doc = create_user_doc(books, book_id2attr)
        dataset.append(doc)
    print_log("dataset size : {}".format(len(dataset)))
    return dataset

def create_user_doc(book_ids, book_id2attr = None):
    '''
    Args:
        book_ids : list of book ids
        book_id2attr : dictionary of {id -> attribute}
    '''
    result = []
    for id in book_ids:
        if book_id2attr and book_id2attr[id]:
            result.append(book_id2attr[id])
        else:
            result.append(id)
    doc = " ".join(result)
    return doc

def get_vocabulary(dataset):
    vocabulary = list(set(" ".join(dataset).split()))
    print_log("vocabulary size : {}".format(len(vocabulary)))
    return vocabulary

def book_id2attr_map(folder_path, attributes=['title']):
    book_data = load_dictionary(glob.glob(folder_path + 'book_data.json')[0])
    print_log('total books loaded = {}'.format(len(book_data)))
    d_list = [dict() for i in range(len(attributes))]
    for key, value in book_data.items():
        for idx, d in enumerate(d_list):
            if attributes[idx]=='description':
                descr = value[attributes[idx]]
                if descr:
                    descr = clean_html(descr.lower())
                d[key] = descr
            else:
                d[key] = value[attributes[idx]]
    return d_list

def analyze_tf(tf):
    tf = tf > 0
    freqs = tf.sum(axis=0).transpose()
    print(freqs.shape)
    n, bins, patches = plt.hist(freqs, 50, facecolor='green')
#    plt.show()

def load_book_data_as_input(folder_path):
    book_data = load_dictionary(glob.glob(folder_path + 'book_data.json')[0])
    dataset= []
    ids = []
    for key, value in book_data.items():
        descr = value['description']
        if descr:
            descr = clean_html(descr.lower())
        else:
            descr = get_name(value['title'].lower())
        dataset.append(descr)
        ids.append(key)
    print_log("dataset size : {}".format(len(dataset)))
    return ids, dataset


def plot_sample_books(book_ids, book_weights, book_id2title ,n=5):
    ids = book_ids[:n]
    weight_matrix = book_weights[:n]
    n_rows, n_cols = 3, 2
    f, axis_arr = plt.subplots(n_rows, n_cols)
    for row in range(n_rows):
        for col in range(n_cols):
            if row+col>=n:
                continue
            axis_arr[row][col].plot(range(weight_matrix.shape[1]),
                 weight_matrix[row+col])
            axis_arr[row][col].set_title(book_id2title[ids[row+col]])
    plt.show()

def plot_users(folder_path):
    all_user_files = glob.glob(folder_path +'user_*.json')
    for fpath in all_user_files:
        d = load_dictionary(fpath)
        user_id, user_name, book_ids = d.keys()[0],\
                                        get_name(d.values()[0]['name']),\
                                        d.values()[0]['books'].keys()
        #TODO: fetch indices of books user has read.
        
                                        
        

if __name__ == "__main__":
    logging.basicConfig(filename='result.log', filemode='w',level=logging.INFO)
    n_topics = 10
    n_top_words = 10
    n_features = 1000
    min_df = 2
    max_df = 0.2
    max_iter = 10
    print_log('n_topics = {}, n_top_words = {}'.format(n_topics, n_top_words))
    print_log('min_df = {}, max_df = {}'.format(min_df, max_df))
    book_id2title, book_id2description = book_id2attr_map(DATA_DIR, attributes=['title','description'])
    
#    dataset = load_user_data(DATA_DIR, book_id2description)
    book_ids, dataset = load_book_data_as_input(DATA_DIR)
    
    vocabulary = get_vocabulary(dataset)
#    print_log(book_id2description['1362'])
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df,
                                    max_features=n_features,
                                    #vocabulary=vocabulary,
                                    stop_words='english')
    t0 = time()
    tf = tf_vectorizer.fit_transform(dataset)
    print_log("done in %0.3fs." % (time() - t0))
    print_log(tf.shape)
    #analyze_tf(tf)

    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=max_iter,
                                learning_method='online',
                                learning_offset=20.,
                                random_state=0)
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))
    
    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
    
    book_weights = lda.fit_transform(tf)
    #plot_sample_books(book_ids, book_weights, book_id2title)
    
    