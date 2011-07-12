from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^', include('profile.urls')),
    url(r'^', include('posts.urls')),
)