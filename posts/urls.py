from django.conf.urls.defaults import *
from posts.views import *

urlpatterns = patterns('posts.views',
    url(r'^posts/$', view=post, name='post'),
)