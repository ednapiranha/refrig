from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.template import RequestContext

from mongoengine import *
from posts.models import Post, ImagePost, TextPost, LinkPost

from profile.views import *

def posts(request):
    """
    add a new post
    """
    if check_key(request) and request.method == 'POST':
        if request.POST.get('post_type') == 'link':
            post = LinkPost(description=request.POST.get('description'),author=request.session['profile'])
        elif request.POST.get('post_type') == 'image':
            post = ImagePost(description=request.POST.get('description'),author=request.session['profile'])
        else:
            post = TextPost(description=request.POST.get('description'),author=request.session['profile'])
            post.set_autotags
            print post.description
        post.save()

    return HttpResponseRedirect('/dashboard')

def delete(request, post_id):
    """
    delete an existing post
    """    
    if check_key(request):
        try:
            post = Post.objects(author=request.session['profile'], id=post_id).first()
            post.delete()
        except:
            return HttpResponseRedirect('/dashboard')
    return HttpResponseRedirect('/dashboard')