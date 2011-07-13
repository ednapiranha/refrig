from django.conf.urls.defaults import *
from posts.views import *

urlpatterns = patterns('posts.views',
    url(r'^posts/$', view=posts, name='posts'),
    url(r'^posts/delete/(?P<post_id>\w+)/$', view=delete, name='delete'),
    url(r'^tagged/(?P<tag>\w+)/$', view=tagged, name='tagged'),
    url(r'^repost/(?P<post_id>\w+)/$', view=repost, name='repost'),
    url(r'^post/(?P<post_id>\w+)/$', view=show, name='show'),
    url(r'^public/$', view=public, name='public'),
)