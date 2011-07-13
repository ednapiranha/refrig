from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^', include('profile.urls')),
    url(r'^', include('posts.urls')),
)