
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson

from qr import settings
from qr.games import test_helpers
from qr.games.models import *

class TestView_game_list(TestCase):
    url = reverse('game_list')
    
    def setUp(self):
        test_helpers.create_users(self)
        test_helpers.create_games(self)

        self.response = self.client.get(self.url)
    
    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/list.html')
    
    def test_context(self):
        test_helpers.check_context(self, ['game_list'])
    
    def test_no_games_listed(self):
        # delete the games & then get a new list
        Game.objects.all().delete()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, 'No games')
    
    def test_all_games_listed(self):
        for game in Game.objects.all():
            self.assertContains(self.response, game.city)

    def test_anon_user_gets_no_edit_links(self):
        for game in Game.objects.all():
            edit_link = reverse('game_edit',
                                kwargs={'game_id':game.id})
            self.assertNotContains(self.response, edit_link)

    def test_logged_in_user_gets_correct_edit_links(self):
        # login a user, then get a new list
        user = User.objects.get(pk=1)
        self.assertTrue(
            self.client.login(username=user.username,
                              password=user.username))
        self.response = self.client.get(self.url)
        
        # for each game, check if the edit link exists when
        # it should. Also, we should have at least one of each
        # (otherwise the test data we're using isn't very useful)
        contain_count = 0
        not_contain_count = 0
        for game in Game.objects.all():
            edit_link = reverse('game_edit',
                                kwargs={'game_id':game.id})
            if game.created_by == user:
                self.assertContains(self.response, edit_link)
                contain_count += 1
            else:
                self.assertNotContains(self.response, edit_link)
                not_contain_count += 1
        
        self.assertTrue(contain_count > 0)
        self.assertTrue(not_contain_count > 0)
        


class TestView_create_game(TestCase):
    url = reverse('game_create')
    
    def setUp(self):
        test_helpers.create_users(self)

        # most tests will need a response from a logged-in user
        self.user = User.objects.get(pk=1)
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/create.html')

    def test_context(self):
        test_helpers.check_context(self, ['form', 'gmap_js'])

    def test_game_creation(self):
        # shouldn't be any games yet
        self.assertEqual(Game.objects.count(), 0)
        
        # POST data to create a game
        point_data = [ { 'id' : '0',
                         'lat' : '12.34533',
                         'lon' : '-0.32112' } ]
        form_data = { 'game_type' : GAME_TYPES[0][0],
                      'is_public' : True,
                      'city' : 'calgary',
                      'locations' : simplejson.dumps(point_data) }
        self.response = self.client.post(self.url, form_data, follow=True)
        
        # a game should have been created in the database
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.all()[0]
        self.assertEqual(form_data['game_type'], game.game_type)
        self.assertEqual(form_data['is_public'], game.is_public)
        self.assertEqual(form_data['city'], game.city)
        self.assertEqual(point_data[0]['lat'], str(game.center_latitude))
        self.assertEqual(point_data[0]['lon'], str(game.center_longitude))
        self.assertEqual(self.user, game.created_by)
        
        # we should be redirected to the game editing page
        expUrl = reverse('game_edit', args=(game.id,))
        self.assertRedirects(self.response, expUrl)
    
    def test_anon_user_redirected(self):
        self.client.logout()
        self.response = self.client.get(self.url)
        expUrl = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(self.response, expUrl)

class TestView_game_details(TestCase):
    url = 'game_details'    # actual URL set in setUp()
    
    def setUp(self):
        test_helpers.create_users(self)
        test_helpers.create_games(self)
        
        # most tests will need a response from a logged-in user,
        # who is NOT the creator of the game
        self.game = Game.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.assertNotEqual(self.user, self.game.created_by)
        self.url = reverse(self.url, args=(self.game.pk,))
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/details.html')

    def test_context(self):
        test_helpers.check_context(self, ['game', 'players', 'can_join_game'])

    def test_game_creator_cannot_join(self):
        # logout user2 and login the creator of the game
        self.client.logout()
        self.user = self.response.context['game'].created_by
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)
        
        self.assertFalse(self.response.context['can_join_game'])

    def test_other_user_can_join_game(self):
        # we are by default not a member of the game,
        # so we should be able to join it
        self.assertTrue(self.response.context['can_join_game'])
    
    def test_user_cannot_join_game_twice(self):
        # join the game
        player = Player(game=self.game, user=self.user)
        player.save()
        
        # get the page again, but we should not be able to join
        self.response = self.client.get(self.url)
        self.assertFalse(self.response.context['can_join_game'])
        
        # do a POST request to join the game, it shouldn't add another Player
        form_data = { 'mode' : 'join' }
        self.response = self.client.post(self.url, form_data)
        self.assertEqual(self.response.status_code, 200)
        player = Player.objects.filter(game__exact=self.game,
                                       user__exact=self.user)
        self.assertEqual(player.count(), 1)

    def test_user_joins_game(self):
        # POST a request to join the game
        form_data = { 'mode' : 'join' }
        self.response = self.client.post(self.url, form_data)
        self.assertEqual(self.response.status_code, 200)
        
        # make sure the Player got created
        player = Player.objects.filter(game__exact=self.game,
                                       user__exact=self.user)
        self.assertEqual(player.count(), 1)
        
        # make sure the returned page doesn't allow the
        # user to join again
        self.assertFalse(self.response.context['can_join_game'])

