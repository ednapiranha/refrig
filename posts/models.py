from mongoengine import *
from profile.models import *

from BeautifulSoup import BeautifulSoup

import re
import datetime
from urlparse import urlparse

VALID_TAGS = []
PAGE_LIMIT = 20

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
    original_id = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'ordering': ['-created_at']
    }
    
    def save_tags(self):
        tags = []
        tags_array = self.tags.split(",")
        for tag in tags_array:
            tags.append(tag.lower().strip())
        self.tags = tags
    
    @staticmethod
    def save_by_pattern(request):
        """
        we only care about 4 types of post submissions - images, videos, links and plain text.
        the first 3 are link types but treated in post-render differently.
        """
        check_link = urlparse(request.POST.get('description'))
     
        if check_link.scheme == 'http' and Post.__is_image(check_link):
            post = ImagePost(description=request.POST.get('description'))
        elif check_link.scheme == 'http' and ('vimeo' in check_link.netloc or 'youtube' in check_link.netloc):
            post = VideoPost(description=request.POST.get('description'))
        elif check_link.scheme == 'http':
            post = LinkPost(description=request.POST.get('description'))
        else:
            post = TextPost(description=request.POST.get('description'))
        post.author = request.session['profile']
        post.tags = request.POST.get('tags')
        post.save_tags()
        post.save()
    
    def save_repost(self, user):
        if not self.is_private:
            if self.original_author:
                original_author = self.original_author
                original_id = self.original_id
            else:
                original_author = self.author
                original_id = self.id
            if isinstance(self, LinkPost):
                post = LinkPost(description=self.description,author=user,tags=self.tags,original_author=original_author,original_id=str(original_id))
            elif isinstance(self, ImagePost):
                post = ImagePost(description=self.description,author=user,tags=self.tags,original_author=original_author,original_id=str(original_id))
            else:
                post = TextPost(description=self.description,author=user,tags=self.tags,original_author=original_author,original_id=str(original_id))

            post.save()

    @staticmethod
    def tagged_posts(tag, page=1):
        total_posts = Post.objects(tags=tag).count()
        posts = Post.objects(tags=tag).skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        return [posts, total_posts]
        
    @staticmethod
    def my_posts(user, viewer, page=1):
        if user == viewer:
            total_posts = Post.objects(author=user).count()
            posts = Post.objects(author=user).skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        else:
            total_posts = Post.objects(author=user).count()
            posts = Post.objects(author=user).skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        return [posts, total_posts]
    
    @staticmethod
    def public_posts(page=1):
        total_posts = Post.objects.count()
        posts = Post.objects.skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        return [posts, total_posts]

    @staticmethod
    def __is_image(check_link):
        try:
            if check_link.path.lower().index('jpg') or check_link.path.lower().index('jpeg') or check_link.path.lower().index('gif') or check_link.path.lower().index('png'):
                return True
        except:
            return False
    
class TextPost(Post):
    description = StringField(required=True)

class ImagePost(Post):
    description = StringField()

class LinkPost(Post):
    description = StringField()

class VideoPost(Post):
    description = StringField()