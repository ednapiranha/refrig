from django.http import *
from django import template
from django.template.defaultfilters import stringfilter
from django.template import RequestContext 

from mongoengine import *
from profile.models import Profile
from posts.models import Post, ImagePost, TextPost, LinkPost
from profile.views import *

import tweepy

from profile.views import *

register = template.Library()

@register.filter
@stringfilter
def generate_post(value, post):
    # determine which output to generate based on the post type
    if isinstance(post, ImagePost):
        media = '<img src="'+post.description+'" alt="'+post.description+'" />'
    elif isinstance(post, LinkPost):
        media = '<a href="'+post.description+'">'+post.description+'</a>'
    else:
        media = '<p>'+'<br />'.join(post.description.split("\n"))+'</p>'
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
    if post.original_author:
        repost_count = str(Post.objects(original_id=post.original_id,original_author=post.original_author).count())
        result = '<span class="repost_count">'+repost_count+'</span> Originally posted by <a href="/user/'+str(post.original_author.id)+'">'+post.original_author.full_name+'</a>'
    else:
        result = ''
    return result
