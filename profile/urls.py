from django.conf.urls.defaults import *
from profile.views import *

urlpatterns = patterns('profile.views',
    url(r'^$', view=index, name='index'),
    url(r'^callback/$', view=callback, name='auth_return'),
    url(r'^logout/$', view=unauth, name='oauth_unauth'),
    url(r'^auth/$', view=auth, name='oauth_auth'),
    url(r'^dashboard/$', view=dashboard, name='dashboard'),
)