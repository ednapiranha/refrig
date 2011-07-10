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
    if check_key(request):
        post = Post(message=request.POST.get('message'),author=request.session['profile'])
        post.save()
        posts = Post.objects(author=request.session['profile']).order_by("+created_at")

        return render_to_response('profile/dashboard.html', {
            'posts' : posts, 
            'user' : request.session['profile']
        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('profile/index'))