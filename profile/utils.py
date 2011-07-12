from django.conf import settings

from mongoengine import *
from profile.models import Profile

import tweepy

def get_api(request):
    # set up and return a twitter api object
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    access_key = request.session['access_key_tw']
    access_secret = request.session['access_secret_tw']
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth)

    try:
        request.session['profile'] = Profile.objects.get_or_create(
            access_key=access_key, 
            access_secret=access_secret, 
            profile_image_url=api.me().profile_image_url,
            full_name=api.me().name).first()
    except:
        request.session['profile'] = Profile.objects(
            access_key=access_key, 
            access_secret=access_secret).first()
    return request.session['profile']