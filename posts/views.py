from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.template import RequestContext

from mongoengine import *
from posts.models import Post, ImagePost, TextPost, LinkPost

from profile.views import *

import math

def posts(request):
    """
    add a new post
    """
    if check_key(request):
        if request.method == 'POST':
            Post.save_by_pattern(request)
    return HttpResponseRedirect('/dashboard')

def update(request):
    if check_key(request):
        user = get_api(request)
        if request.method == 'POST':
            post = Post.objects(id=request.POST.get('post_id'), author=user).first()
            post.update_by_pattern(request)
            return HttpResponseRedirect('/post/'+str(post.id))
        else:
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')

def edit(request, post_id):
    """
    edit a post
    """
    if check_key(request):
        user = get_api(request)
        post = Post.objects(id=post_id).first()
        tags = ', '.join(post.tags)
        return render_to_response('posts/edit.html', {
            'post' : post,
            'tags' : tags,
            }, context_instance=RequestContext(request))
    else:
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

def tagged(request, tag, page=1):
    """
    load your posts matching a tag
    """
    if check_key(request):
        user = get_api(request)
    else:
        user = None

    post_item = Post.tagged_posts(tag.lower(), page)
    posts = post_item[0]
    total_posts = post_item[1]
    next_page = page + 1
    prev_page = page - 1
    post_count = math.floor(len(posts) / PAGE_LIMIT)    
        
    return render_to_response('posts/tagged.html', {
        'posts' : posts,
        'user' : user,
        'tag' :  tag,
        'next_page' : next_page,
        'prev_page' : prev_page,
        'post_count': post_count,
        }, context_instance=RequestContext(request))
 
def show(request, post_id):
    """
    load single post
    """ 
    post = [Post.objects(id=post_id).first()]
    if check_key(request):
        user = get_api(request)
    else:
        user = None
        
    return render_to_response('posts/show.html', {
        'posts' : post,
        'user' : user,
        }, context_instance=RequestContext(request))
        
def repost(request, post_id):
    """
    repost a user's post
    """
    if check_key(request):

        user = get_api(request)
        post = Post.objects(id=post_id).first()
        if user != post.author:
            post.save_repost(request.session['profile'])

    return HttpResponseRedirect('/dashboard')

def public(request, page=1):
    """
    display everyone's posts
    """
    if check_key(request):
        user = get_api(request)
    else:
        user = None

    post_item = Post.public_posts(page)
    posts = post_item[0]
    total_posts = post_item[1]
    next_page = page + 1
    prev_page = page - 1
    post_count = math.floor(len(posts) / PAGE_LIMIT)    
        
    return render_to_response('posts/public.html', {
        'posts' : posts,
        'user' : user,
        'next_page' : next_page,
        'prev_page' : prev_page,
        'post_count': post_count,
        }, context_instance=RequestContext(request))