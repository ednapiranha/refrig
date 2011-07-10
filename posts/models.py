from mongoengine import *
from profile.models import *

import datetime

class Comment(EmbeddedDocument):
    message = StringField()
    author = ReferenceField(Profile)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class Post(Document):
    message = StringField(required=True)
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
    description = StringField()

class ImagePost(Post):
    url = StringField()
    description = StringField()

class LinkPost(Post):
    url = StringField()
    description = StringField()