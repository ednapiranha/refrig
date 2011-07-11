from django import template
from django.template.defaultfilters import stringfilter

from mongoengine import *
from profile.models import Profile
from posts.models import Post, ImagePost, TextPost, LinkPost

import tweepy

register = template.Library()

@register.filter
@stringfilter
def generate_post(value, post):
    # determine which output to generate based on the post type
    if isinstance(post, ImagePost):
        value = '<img src="'+post.description+'" alt="'+post.description+'" />'
    elif isinstance(post, LinkPost):
        value = '<a href="'+post.description+'">'+post.description+'</a>'
    else:
        value = '<p>'+post.description+'</p>'
    return value