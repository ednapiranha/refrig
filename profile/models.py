from mongoengine import *

import datetime

class Profile(Document):
    access_key = StringField(unique_with='access_secret')
    access_secret = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    first_name = StringField()
    last_name = StringField()
    profile_image_url = StringField()
