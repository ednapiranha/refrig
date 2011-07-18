from mongoengine import *

import datetime
import inspect

class Profile(Document):
    access_key = StringField(unique_with='access_secret')
    access_secret = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    full_name = StringField()
    profile_image_url = StringField()
    follows = ListField(EmbeddedDocumentField('Profile'))

    meta = {
        'ordering': ['+full_name']
    }
    
    def follow(self, user):
        self.follows.append(user)
        self.save()
 
    def unfollow(self, user):
        self.follows.remove(user)
        self.save()

    def is_following(self, user):
        if user in self.follows:
            return True
        return False