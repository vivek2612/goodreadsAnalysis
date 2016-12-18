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

gc = client.GoodreadsClient(APP_KEY, APP_SECRET)
#print(gc.session.access_token)
#print(gc.session.access_token_secret)
access_token = 'jSWly3TI5LzC16xfQeCw'
access_token_secret = '5D5DkUqHez5pAaE9wIYjaqjBELcamdigTwE4YUAj8'

gc.authenticate(access_token, access_token_secret)
user = gc.auth_user()
print(user.name)
print(user.gid)
my_reviews = user.reviews(page=1)
for review in my_reviews:
    book = GoodreadsBook(review.book, gc)    
    print(book.title)
    print(review.rating)

user = GoodreadsUserExtended.fromBaseUser(user)
friend_list = user.friends(all=False)
for friend in friend_list[:5]:
    print(friend.name, friend.gid)
print("Total friends = {}".format(len(friend_list)))