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
def is_following(value, user):
    # determine if user is already following
    if value.is_following(user):
        follow_link = '<a href="/unfollow/'+str(user.id)+'" class="followed">Unfollow</a>'
    elif user.id != value.id:
        follow_link = '<a href="/follow/'+str(user.id)+'" class="follow">Follow</a>'
    else:
        follow_link = ''
    return follow_link