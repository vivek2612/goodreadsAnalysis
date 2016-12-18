# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 14:51:52 2016

@author: Vivek
"""

from goodreads.user import GoodreadsUser

class GoodreadsUserExtended(GoodreadsUser):
    '''
    Extending the 'GoodreadsUser()' class
    '''
    def __init__(self, user_dict, client):
        GoodreadsUser.__init__(self, user_dict, client)
        self.friend_list = None
        
    @classmethod
    def fromBaseUser(cls, baseUserObject):
        return GoodreadsUserExtended(baseUserObject._user_dict,
                                     baseUserObject._client)
        
    def friends(self, all=True):
        """
        Returns : list of GoodreadsUser() objects.
        Args:
            client : oauth required. therefore, client must be authenticated.
            user : GoodreadsUser() object.    
            all : True if all friends are to be returned. 
                  Else only friends only on the first page are returned.
        """
        url = 'friend/user'
        page_count = 0
        self.friend_list = []
        while True:
            page_count += 1
            params = {'format':'xml', 'id':self.gid, 'page':page_count}   
            resp = self._client.request_oauth(url, params)
            user_friends = resp['friends']['user']
            for friend in user_friends:
                f = GoodreadsUser(friend, self._client)
                f.user_name = f.name
                self.friend_list.append(f)
            total_friends = int(resp['friends']['@total'])
            if len(self.friend_list) >= total_friends or not all:
                break
        return self.friend_list