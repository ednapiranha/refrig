from mongoengine import *
from profile.models import *

from BeautifulSoup import BeautifulSoup

import re
import datetime

VALID_TAGS = []
p_tags = re.compile('(<p>)|(</p>)')

class Comment(EmbeddedDocument):
    message = StringField()
    author = ReferenceField(Profile)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

class Post(Document):
    author = ReferenceField(Profile)
    original_author = ReferenceField(Profile)
    tags = ListField(StringField(max_length=50))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'ordering': ['-created_at']
    }
    
    def save_tags(self):
        tags = []
        tags_array = self.tags.split(",")
        for tag in tags_array:
            tags.append(tag.strip())
        self.tags = tags
    
    def save_repost(self, user):
        if isinstance(self, LinkPost):
            post = LinkPost(description=self.description,author=user,tags=self.tags,original_author=self.author)
        elif isinstance(self, ImagePost):
            post = ImagePost(description=self.description,author=user,tags=self.tags,original_author=self.author)
        else:
            post = TextPost(description=self.description,author=user,tags=self.tags,original_author=self.author)
        post.save()
    
    @staticmethod
    def tagged_posts(user, tag):
        posts = Post.objects(author=user,tags=tag)
        return posts
        
    @staticmethod
    def my_posts(user):
        posts = Post.objects(author=user)
        return posts
    
class TextPost(Post):
    description = StringField(required=True)

class ImagePost(Post):
    description = StringField()

class LinkPost(Post):
    description = StringField()