from django.conf import settings

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.template import RequestContext

from profile.models import *
from posts.models import *

from utils import *
import math

def index(request):
    """
    main view of app, either public page or dashboard
    """
    # if we haven't authorised yet, direct to login page
    if check_key(request):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect('/public')
 
def unauth(request):
    """
    logout and remove all session data
    """
    if check_key(request):
        api = get_api(request)
        request.session.clear()
        logout(request)
    return HttpResponseRedirect(reverse('index'))

def yours(request, page=1):
    """
    your posts
    """
    if check_key(request):
        user = get_api(request)

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        post_item = Post.my_posts(user,user,page)
        posts = post_item[0]
        total_posts = post_item[1]
        next_page = page + 1
        prev_page = page - 1
        post_count = math.floor(len(posts) / PAGE_LIMIT)
            
        return render_to_response('profile/dashboard.html', {
            'posts' : posts,
            'user' : user,
            'title' : "Your Posts",
            'next_page' : next_page,
            'prev_page' : prev_page,
            'post_count': post_count,
            'total_posts' : total_posts,
            }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('index'))

def dashboard(request, page=1):
    """
    dashboard followng posts
    """
    if check_key(request):
        user = get_api(request)

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        post_item = Post.dashboard_posts(user,page)
        posts = post_item[0]
        total_posts = post_item[1]
        next_page = page + 1
        prev_page = page - 1
        post_count = math.floor(len(posts) / PAGE_LIMIT)
            
        return render_to_response('profile/dashboard.html', {
            'posts' : posts,
            'user' : user,
            'title' : 'Dashboard',
            'next_page' : next_page,
            'prev_page' : prev_page,
            'post_count': post_count,
            'total_posts' : total_posts,
            }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('index'))

def user_view(request, user_id, page=1):
    """
    display user posts 
    """
    public_user = Profile.objects(id=user_id).first()
    if check_key(request):
        user = get_api(request)
    else:
        user = None
    
    post_item = Post.my_posts(public_user,user,page)    
    posts = post_item[0]
    total_posts = post_item[1]
    next_page = page + 1
    prev_page = page - 1
    post_count = math.floor(len(posts) / PAGE_LIMIT)

    return render_to_response('profile/user_view.html', {
        'posts' : posts,
        'public_user' : public_user,
        'user' : user,
        'next_page' : next_page,
        'prev_page' : prev_page,
        'post_count': post_count,
        'total_posts' : total_posts,
        }, context_instance=RequestContext(request))

def follow(request, user_id):
    """
    follow a user
    """
    if check_key(request):
        user = get_api(request)
        follow_user = Profile.objects(id=user_id).first()
        user.follow(follow_user)

        return HttpResponseRedirect(reverse('community'))
    else:
        return HttpResponseRedirect(reverse('index'))

def unfollow(request, user_id):
    """
    unfollow a user
    """
    if check_key(request):
        user = get_api(request)
        unfollow_user = Profile.objects(id=user_id).first()
        user.unfollow(unfollow_user)

        return HttpResponseRedirect(reverse('community'))
    else:
        return HttpResponseRedirect(reverse('index')) 

def community(request):
    """
    display users
    """ 
    users = Profile.objects
    
    if check_key(request):
        user = get_api(request)
    else:
        user = None
    
    return render_to_response('profile/community.html', {
        'users' : users,
        'user' : user,
        }, context_instance=RequestContext(request))
        
def auth(request):
    # start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    # direct the user to the authentication url
    auth_url = oauth.get_authorization_url()
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret) 
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.set_request_token(token[0], token[1])
    # get the access token and store

    try:
        oauth.get_access_token(verifier)
        # check if user already exists, and load up their info, else set them up in the db
    except tweepy.TweepError:
        print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key  
    request.session['access_secret_tw'] = oauth.access_token.secret
    response = HttpResponseRedirect(reverse('dashboard'))
    return response

def check_key(request):
    """
    Check to see if we already have an access_key or user profile stored, if we do then we have already gone through OAuth. If not then we haven't and we probably need to.
    """

    try:
        if not request.session.get('profile', None):
            if not request.session.get('access_key_tw', None):
                return False
    except KeyError:
        return False
    return True
