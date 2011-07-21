from django.http import *
from django import template
from django.template.defaultfilters import stringfilter
from django.template import RequestContext 

from mongoengine import *
from profile.models import Profile
from posts.models import Post, ImagePost, TextPost, LinkPost
from profile.views import *

import tweepy

from urlparse import urlparse

register = template.Library()

@register.filter
def generate_post(value, post):
    # determine which output to generate based on the post type
    if isinstance(post, ImagePost):
        media = '<img src="'+post.description+'" alt="'+post.description+'" />'
    elif isinstance(post, LinkPost):
        media = '<a href="'+post.description+'">'+post.description+'</a>'
    elif isinstance(post, VideoPost):
        url = urlparse(post.description)
        if post.description.lower().find('vimeo') > -1:
            media = '<iframe src="http://player.vimeo.com/video/'+str(url.path.strip('/'))+'?wmode=transparent" width="70%" height="300"></iframe>'
        elif post.description.lower().find('youtube') > -1:
            media = '<iframe class="youtube-player" type="text/html" width="70%" height="300" src="http://youtube.com/embed/'+str(url.query.split('&')[0].split('v=')[1])+'"></iframe>'
    elif isinstance(post, AudioPost):
        if post.description.endswith('mp3'):
            audio_type = 'audio/mpeg'
        else:
            audio_type = 'audio/ogg'
        media = '<audio controls="controls" preload="auto"><source src="'+post.description+'" type="'+audio_type+'" /></audio>'
    else:
        media = '<p>'+post.description+'</p>'
    return media
    
@register.filter
def generate_tags(value, post):
    # generate tags output from list
    tag_list = post.tags
    tags = ''
    for tag in tag_list:
        if len(tag) > 0:
            tags += '<a href="/tagged/'+tag+'">'+tag+'</a> '
    return tags

@register.filter
def generate_meta_response(value, post):
    # output the original author if it exists
    result = '<a class="details" href="/post/'+ str(post.id) +'" title="details">D</a> '
    if post.original_author:
        repost_count = str(Post.objects(original_id=post.original_id,original_author=post.original_author).count())
        result += '<span class="repost_count">'+repost_count+'</span> <span class="repost_info">Originally posted by <a href="/user/'+str(post.original_author.id)+'">'+post.original_author.full_name+'</a></span>'
    return result
