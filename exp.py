# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:25:38 2016

@author: Vivek
"""

from config import APP_KEY, APP_SECRET
from goodreads import client
from goodreads.book import GoodreadsBook
from goodreads.review import GoodreadsReview
from user_extended import GoodreadsUserExtended
import json
from collections import OrderedDict
import logging
from utility import print_log
from utility import get_name, easy_json

def save_dictionary(data, fpath):
    with open(fpath, 'w') as f:
        json.dump(data, f)
    print_log("Saved as {}".format(fpath))

def load_dictionary(fpath):
    try:
        with open(fpath) as f:
            data = json.load(f)
            return data
    except:
        print_log('error : could not load file at {}'.format(fpath))

def extract_book_info(book):
    '''
    book : GoodreadsBook() object
    Returns:
        {title="", description="", authors=[], average_rating=1}
    '''
    info = {}
    info['title'] = book.title
    info['description'] = book.description
    info['authors'] = [author.gid for author in book.authors]
    info['average_rating'] = book.average_rating
    return info

def extract_author_info(author):
    '''
    author : GoodreadsAuthor() object
    Returns:
        {name="", gender="", books=[], works_count=10}
    '''
    info = {}
    info['name'] = author.name
    info['average_rating'] = author._author_dict['average_rating']
    return info

    
DATA_DIR = 'E:/spyder_workspace/goodreads/goodreadsAnalysis/data/'
ACCESS_TOKEN = 'jSWly3TI5LzC16xfQeCw'
ACCESS_TOKEN_SECRET = '5D5DkUqHez5pAaE9wIYjaqjBELcamdigTwE4YUAj8'
book_data = {}
author_data = {}
    
def get_reviews(gc, user_id='29400625'):
    user = GoodreadsUserExtended.fromBaseUser(gc.user(user_id))
    reviews = user.reviews()
    for review  in reviews:
        print_log(easy_json(review.book))
        return
        
def collect_reviews(gc, all_ids):
    '''
    all_ids : list of user_ids for which reviews are needed.
    '''
    global book_data, author_data
    for user_id in all_ids:
        friend = GoodreadsUserExtended.fromBaseUser(gc.user(user_id))
        print_log("{} ".format((get_name(friend.name), friend.gid)))
        user_data = {}
        user_data[friend.gid] = {'name':friend.name, 'books':{}}
        user_reviews = friend.reviews(page='all')
        for i, review in enumerate(user_reviews):
            try:
                book = GoodreadsBook(review.book, gc)
                if isinstance(book.gid, OrderedDict):
                    book.gid = dict(book.gid)['#text']
                if not book_data.has_key(book.gid):
                    book_data[book.gid] = extract_book_info(book)
                user_data[friend.gid]['books'][book.gid] = review.rating
                for author in book.authors:
                    if not author_data.has_key(author.gid):
                        author_data[author.gid] =  extract_author_info(author)
            except:
                print_log("error : review for friend_id={} review_dict {}".format(friend.gid,
                          review._review_dict))
        friend_name = '_'.join(get_name(friend.name).split()).lower()
        fname = DATA_DIR + 'user_{}_{}.json'.format(friend_name, friend.gid)
        save_dictionary(user_data, fname)
    save_dictionary(book_data, DATA_DIR + 'book_data.json')
    save_dictionary(author_data, DATA_DIR + 'author_data.json')
    
if __name__ == "__main__":    
    logging.basicConfig(filename='result.log', level=logging.INFO)
    gc = client.GoodreadsClient(APP_KEY, APP_SECRET)
    #print_log(gc.session.access_token)
    #print_log(gc.session.access_token_secret)
    
    gc.authenticate(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    user = gc.auth_user()
    print_log("Hello I am {} with id = {}".format(user.name, user.gid))
    user = GoodreadsUserExtended.fromBaseUser(user)
    
    friend_list = user.friends(all=True)
    all_ids = [u.gid for u in friend_list+[user]]
    collect_reviews(gc, all_ids)
    print_log('total books = {}'.format(len(book_data)))    
    print_log('total authors = {}'.format(len(author_data)))
    print_log('total users = {}'.format(len(all_ids)))
    exit()    
        