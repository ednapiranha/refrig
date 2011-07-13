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
            post = LinkPost(description=request.POST.get('description'),author=request.session['profile'],tags=request.POST.get('tags'))
        elif request.POST.get('post_type') == 'image':
            post = ImagePost(description=request.POST.get('description'),author=request.session['profile'],tags=request.POST.get('tags'))
        else:
            post = TextPost(description=request.POST.get('description'),author=request.session['profile'],tags=request.POST.get('tags'))
        post.save_tags()
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

def tagged(request, tag, page=1):
    """
    load your posts matching a tag
    """
    if check_key(request):
        user = request.session['profile']
    else:
        user = None
    
    posts = Post.tagged_posts(tag.lower())
    next_page = page + 1
    prev_page = page - 1
    post_count = len(posts)    
        
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
        user = request.session['profile']
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
        try:
            user = request.session['profile']
            post = Post.objects(id=post_id).first()
            if user != post.author:
                post.save_repost(request.session['profile'])
        except:
            return HttpResponseRedirect('/dashboard')
    return HttpResponseRedirect('/dashboard')