from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson

from django.test.client import Client

class TestView_Base(TestCase):
    fixtures = ['test_data/users.xml']
    url = reverse('game_list')
    
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

        self.response = self.client.get(self.url)
        
        self.assertTrue(User.objects.all().count() > 0)

    # Make sure the page exists
    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'base.html')
                            
#    def test_context(self):
#        check_context(self, ['base'])

    def test_login(self):
        # Issue a GET request.
        self.response = self.client.post('/login/', {'username': 'test', 'password': 'pass'})
        self.assertEqual(self.response.status_code, 200)
