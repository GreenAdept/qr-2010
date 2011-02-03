from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson

from django.test.client import Client

from test_helpers import create_users

class TestIndex_Page(TestCase):
    url = reverse('game_list')
    
    def setUp(self):
        create_users(self)
        
        # Every test needs a client.
        self.client = Client()
        self.response = self.client.get(self.url)
        self.assertTrue(User.objects.all().count() > 0)

    # Make sure the page exists
    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'base.html')
                            
    def test_login(self):
        self.response = self.client.post('/login/', {'UserName': 'test', 'Password': 'pass'})
        self.assertEqual(self.response.status_code, 200)

    def test_registration(self):
        self.response = self.client.post('/registration/', 
                                         {'UserName': 'test', 'Email': 'test@home', 'Password': 'pass', 'FirstName': 'thing', 'LastName': 'one'})
        self.assertEqual(self.response.status_code, 200);
        
    def test_link_game(self):
        self.response = self.client.post('/game/')
        self.assertEqual(self.response.status_code, 200)
        
    def test_link_contact(self):
        self.response = self.client.post('/contact/')
        self.assertEqual(self.response.status_code, 200)

# This is for when we implement the /about/ page
#    def test_link_about(self):
#        self.response = self.client.post('/about/')
#        self.assertEqual(self.response.status_code, 200)
