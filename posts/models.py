from mongoengine import *
from profile.models import *

from BeautifulSoup import BeautifulSoup

import re
import datetime

from urlparse import urlparse

VALID_TAGS = []
PAGE_LIMIT = 20
TAG_REGEX = re.compile(r'\w+')

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
        'ordering': ['-updated_at']
    }
    
    def save_tags(self):
        tags = []
        tags_list = re.findall(r'\w+', self.tags.lower())
        unique_tags_list = list(Set(tags_list))
        for tag in unique_tags_list:
            tags.append(tag)
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
        elif check_link.scheme == 'http' and Post.__is_video(check_link):
            post = VideoPost(description=request.POST.get('description'))
        elif check_link.scheme == 'http':
            post = LinkPost(description=request.POST.get('description'))
        else:
            post = TextPost(description=request.POST.get('description'))
        post.author = request.session['profile']
        post.tags = request.POST.get('tags')
        post.save_tags()
        post.save()

    def update_by_pattern(self, request):
        """
        update post
        """

        if check_link.scheme == 'http' and Post.__is_image(check_link):
            post = ImagePost(id=self.id,description=request.POST.get('description'),author=self.author)
        elif check_link.scheme == 'http' and Post.__is_video(check_link):
            post = VideoPost(id=self.id,description=request.POST.get('description'),author=self.author)
        elif check_link.scheme == 'http':
            post = LinkPost(id=self.id,description=request.POST.get('description'),author=self.author)
        else:
            post = TextPost(id=self.id,description=request.POST.get('description'),author=self.author)
        post.tags = request.POST.get('tags')
        post.save_tags()
        post.save()
    
    def save_repost(self, user):
        """
        reposts can only be made on posts that were never originally your own
        """
        if self.original_author:
            original_author = self.original_author
            original_id = self.original_id
        else:
            original_author = self.author
            original_id = self.id

        if original_author != user:
            if isinstance(self, ImagePost):
                post = ImagePost()
            elif isinstance(self, LinkPost):
                post = LinkPost()
            elif isinstance(self, VideoPost):
                post = VideoPost()
            else:
                post = TextPost()
            post.description = self.description
            post.tags = self.tags
            post.author = user
            post.original_author = original_author
            post.original_id = str(original_id)
            post.updated_at = datetime.datetime.now()
  
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
    
    @staticmethod
    def __is_video(check_link):
        if 'vimeo' in check_link.netloc or 'youtube' in check_link.netloc:
            return True
        else:
            return False
    
class TextPost(Post):
    description = StringField(required=True)

class ImagePost(Post):
    description = StringField()

class LinkPost(Post):
    description = StringField()

class VideoPost(Post):
    description = StringField()