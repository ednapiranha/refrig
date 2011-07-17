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
        self.Profile.drop_collection()
        self.Post.drop_collection()
        self.user = Profile(access_key=self.test_access_key, access_secret=self.test_access_secret, full_name=self.test_full_name)
        self.user.save()
        self.client = Client()

    def test_not_logged_in(self):
        """
        Test that user is redirected to the homepage if they are attempting to access a page that requires authentication
        """
        path = '/dashboard/'
        response = self.client.get(path, {})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)
  
        path = '/'
        response = self.client.get(path, {})
        self.assertTemplateUsed(response, "profile/login.html")
        
    def test_logged_in_dashboard(self):
        """
        Test that a logged in user lands on the dashboard
        """
        path = '/dashboard/'
        session = self.client.session
        session['profile'] = self.user
        session.save()
        
        response = self.client.get(path, {})

        self.assertTemplateUsed(response, "profile/dashboard.html")