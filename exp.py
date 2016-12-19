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

gc = client.GoodreadsClient(APP_KEY, APP_SECRET)
#print(gc.session.access_token)
#print(gc.session.access_token_secret)
access_token = 'jSWly3TI5LzC16xfQeCw'
access_token_secret = '5D5DkUqHez5pAaE9wIYjaqjBELcamdigTwE4YUAj8'
DATA_DIR = 'E:/spyder_workspace/goodreads/goodreadsAnalysis/data/'

gc.authenticate(access_token, access_token_secret)
user = gc.auth_user()
print(user.name)
print(user.gid)
user = GoodreadsUserExtended.fromBaseUser(user)
my_reviews = []#user.reviews(page='all')
for review in my_reviews:
    book = GoodreadsBook(review.book, gc)  
    print(book.title)
    print(review.rating)

book_data = {}
author_data = {}

def save_dictionary(data, fpath):
    with open(fpath, 'w') as f:
        json.dump(data, f)
    print("Saved as {}".format(fpath))

def load_dictionary(fpath):
    try:
        with open(fpath) as f:
            data = json.load(f)
            return data
    except:
        print('Could not load file at {}'.format(fpath))

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
    
friend_list = user.friends(all=True)
for _friend in friend_list + [user]:
    friend = GoodreadsUserExtended.fromBaseUser(_friend)
    print(friend.name, friend.gid)
    user_data = {}
    user_data[friend.gid] = {'name':friend.name, 'books':{}}
    user_reviews = friend.reviews(page='all')
    for review in user_reviews:
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
            print(review._review_dict)
                
    fname = DATA_DIR + 'user_{}.json'.format(friend.gid)
    save_dictionary(user_data, fname)

save_dictionary(book_data, DATA_DIR + 'book_data.json')
save_dictionary(author_data, DATA_DIR + 'author_data.json')

print(json.dumps(author_data, indent=4))