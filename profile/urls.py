from django.conf.urls.defaults import *
from profile.views import *

urlpatterns = patterns('profile.views',
    url(r'^$', view=index, name='index'),
    url(r'^callback/$', view=callback, name='auth_return'),
    url(r'^logout/$', view=unauth, name='oauth_unauth'),
    url(r'^auth/$', view=auth, name='oauth_auth'),
    url(r'^dashboard/$', view=dashboard, name='dashboard'),
    url(r'^yours/$', view=yours, name='yours'),
    url(r'^user/(?P<user_id>\w+)/$', view=user_view, name='user_view'),
    url(r'^community/$', view=community, name='community'),
    url(r'^follow/(?P<user_id>\w+)/$', view=follow, name='follow'),
    url(r'^unfollow/(?P<user_id>\w+)/$', view=unfollow, name='unfollow'),
)