from mongoengine import *
from profile.models import *
from posts.models import *

from django.template import RequestContext

from django.test.client import Client
from django.test import TestCase

from utils import *

class TestProfile(TestCase):
    test_access_key = '111'
    test_access_secret = '222'
    test_full_name = 'ginsberg'
    
    def setUp(self):
        self.user = Profile(access_key=self.test_access_key, access_secret=self.test_access_secret, full_name=self.test_full_name)
        self.user.save()
        self.client = Client()
    
    def tearDown(self):
        Profile.objects.delete()
        Post.objects.delete()
