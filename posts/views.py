from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from mongoengine import *
from posts.models import Post, Comment

from utils import *

def posts(request):
    """
    add a new post
    """
    if check_key(request):
        post = Post(message=request.GET.get('message'),author=request.session['profile'])
        return render_to_response('profile/dashboard.html', {'post' : post, 'user' : request.session['profile'] })
    else:
        return HttpResponseRedirect(reverse('profile/index'))