# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:25:38 2016

@author: Vivek
"""

from config import APP_KEY, APP_SECRET
from goodreads import client
from goodreads.book import GoodreadsBook

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
    try:
        print(book.title)
        print(book.description)
        print(book.average_rating)
        print("rating = {}".format(review.rating))
    except:
        print('error')
    print('=================')
print(len(my_reviews))

    

def get_friend_list(user, client):
    """
    Returns : list of GoodreadsUser() objects.
    Args:
        client : oauth required. therefore, client must be authenticated.
        user : GoodreadsUser() object.        
    """
    from goodreads.user import GoodreadsUser
    url = 'friend/user'
    page_count = 0
    friend_list = []
    while True:
        page_count += 1
        params = {'format':'xml', 'id':user.gid, 'page':page_count}   
        resp = client.request_oauth(url, params)
        user_friends = resp['friends']['user']
        for friend in user_friends:
            f = GoodreadsUser(friend, client)
            f.user_name = f.name
            friend_list.append(f)
        total_friends = int(resp['friends']['@total'])
        if len(friend_list) >= total_friends:
            break
    return friend_list
        
friend_list = get_friend_list(user, gc)
for friend in friend_list[:5]:
    print(friend.name, friend.gid)
    print(friend.reviews())
print("Total friends = {}".format(len(friend_list)))

#user = gc.user(1)
#print(user.user_name)