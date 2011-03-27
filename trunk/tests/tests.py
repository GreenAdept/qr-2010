from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson

from django.test.client import Client

from test_helpers import create_users, check_context

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
                                         {'UserName': 'test', 'Email': 'test@home', 'Password': 'pass', 'FirstName': 'thing', 'LastName': 'one', 'Gender':'Female', 'Bio':'biobio', 'Day':'03', 'Month':'05', 'Year':'1985'})
        self.assertEqual(self.response.status_code, 200)
        
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


class TestView_user_profile(TestCase):
    url = ''    # actual URL set in setUp()
    view = 'user_profile'

    def setUp(self):
        create_users(self)
        self.user = User.objects.get(pk=1)
        self.url = reverse(self.view, args=(self.user.username,))
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'users/profile.html')
              
              
class TestView_user_registration(TestCase):
    url = reverse('qr.user_management.registration')


    def setUp(self):
        
        self.client = Client()

        self.response = self.client.post('/registration/', {'UserName': 'test' , 'Password' : 'testing','FirstName' : 'first', 'LastName' : 'last', 'Email' : 'test@gmail.com', 'Gender':'Female', 'Bio':'biobio', 'Day':'03', 'Month':'05', 'Year':'1985', 'Photo' : '/static/profile_pics/10024AI.jpg'})

        #self.user = self.response.context.User

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'users/registration.html')


