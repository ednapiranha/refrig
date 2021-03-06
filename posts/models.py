from mongoengine import *
from profile.models import *

from BeautifulSoup import BeautifulSoup
from web_imagery import web_imagery as wb

import re
import datetime

from urlparse import urlparse

from sets import Set

VALID_TAGS = []
PAGE_LIMIT = 15
TAG_REGEX = re.compile(r'\w+')

class Post(Document):
    author = ReferenceField(Profile)
    original_author = ReferenceField(Profile)
    tags = ListField(StringField(max_length=50))
    original_id = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'ordering': ['-created_at']
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
        description = request.POST.get('description').strip()
        check_link = urlparse(description)
     
        if 'http' in check_link.scheme:
            image = Post.__is_image(description)
            if image != False:
                post = ImagePost(description=Post.__get_image(image))
            elif Post.__is_video(check_link):
                post = VideoPost(description=description)
            elif Post.__is_audio(check_link):
                post = AudioPost(description=description)
            else:
                post = LinkPost(description=description)
        else:
            post = TextPost(description=description)
        post.author = request.session['profile']
        post.tags = request.POST.get('tags')
        post.save_tags()
        post.save()
        for tag in post.tags:
            Tag.add_or_update(tag)

    def update_by_pattern(self, request):
        """
        update post
        """
        description = request.POST.get('description').strip()
        check_link = urlparse(description)

        if 'http' in check_link.scheme:
            image = Post.__is_image(description)
            if image != False:
                post = ImagePost(id=self.id,description=Post.__get_image(image))
            elif Post.__is_video(check_link):
                post = VideoPost(id=self.id,description=description)
            elif Post.__is_audio(check_link):
                post = AudioPost(id=self.id,description=description)
            else:
                post = LinkPost(id=self.id,description=description)
        else:
            post = TextPost(id=self.id,description=description)
        post.author = self.author
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
            elif isinstance(self, AudioPost):
                post = AudioPost()
            else:
                post = TextPost()
            post.description = self.description
            post.tags = self.tags
            post.author = user
            post.original_author = original_author
            post.original_id = str(original_id)
            post.updated_at = datetime.datetime.now()
  
            post.save()
            return post
        else:
            return False

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
    def dashboard_posts(user, page=1):
        total_posts = Post.objects(author__in=user.follows).count()
        posts = Post.objects(author__in=user.follows).skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        return [posts, total_posts]
    
    @staticmethod
    def public_posts(page=1):
        total_posts = Post.objects.count()
        posts = Post.objects.skip((page-1)*PAGE_LIMIT).limit(PAGE_LIMIT)
        return [posts, total_posts]

    @staticmethod
    def __is_image(check_link):
        try:
            image = wb.WebImagery()
            if image.set_image(check_link):
                return image
            else:
                return False
        except:
            return False
            
    @staticmethod
    def __get_image(image):
        return image.get_image()
    
    @staticmethod
    def __is_video(check_link):
        if 'vimeo' in check_link.netloc or 'youtube' in check_link.netloc:
            return True
        else:
            return False
    
    @staticmethod
    def __is_audio(check_link):
        if check_link.path.lower().endswith('mp3') or check_link.path.lower().endswith('ogg'):
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
    
class AudioPost(Post):
    description = StringField()
    
class Tag(Document):
    name = StringField(required=True)
    total_count = IntField(min_value=0)
    
    meta = {
        'ordering': ['-total_count']
    }
    
    @staticmethod
    def add_or_update(tag):
        tag_exist = Tag.objects(name=tag.lower()).first()

        if tag_exist is None:
            Tag.objects.create(name=tag.lower(), total_count=1)
        else:
            total_count = tag_exist.total_count + 1
            tag_exist.total_count = total_count
            tag_exist.save()