from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.template import RequestContext

from mongoengine import *
from posts.models import Post

from profile.views import *

def posts(request):
    """
    add a new post
    """
    if check_key(request) and request.method == 'POST':
        post = Post(message=request.POST.get('message'),author=request.session['profile'])
        post.save()

    return HttpResponseRedirect('/dashboard')

def delete(request, post_id):
    """
    delete an existing post
    """    
    if check_key(request):
        post = Post.objects(author=request.session['profile'], id=post_id).first()
        post.delete()
        
    return HttpResponseRedirect('/dashboard')