from mongoengine import *
from profile.models import *

from BeautifulSoup import BeautifulSoup
from auto_tagify import AutoTagify

import re
import datetime

VALID_TAGS = ['p', 'a']
tag = AutoTagify()
tag.link = '/tags'
tag.css = 'tag'
p_tags = re.compile('(<p>)|(</p>)')

class Comment(EmbeddedDocument):
    message = StringField()
    author = ReferenceField(Profile)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class Post(Document):
    author = ReferenceField(Profile)
    tags = ListField(StringField(max_length=50))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'ordering': ['-created_at']
    }
    
    @staticmethod
    def my_posts(user):
        posts = Post.objects(author=user)
        return posts
    
class TextPost(Post):
    description = StringField(required=True)
    
    def set_autotags(self):
        clean_text = BeautifulSoup(self.description)
        for t in clean_text.findAll(True):
            if t.name not in VALID_TAGS: t.hidden = True
        self.description = tag.generate()

class ImagePost(Post):
    description = StringField()

class LinkPost(Post):
    description = StringField()