
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson
from django.db import IntegrityError

from qr.games import utils
from qr.games.test_helpers import create_games
from qr.tests.test_helpers import create_users, check_context
from qr import settings
from qr.games.models import *

class TestView_game_list(TestCase):
    url = reverse('game_list')
    
    def setUp(self):
        create_users(self)
        create_games(self)

        self.response = self.client.get(self.url)
    
    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/list.html')
    
    def test_context(self):
        check_context(self, ['game_list'])
    
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
        


class TestView_game_create(TestCase):
    url = reverse('game_create')
    
    def setUp(self):
        create_users(self)

        # most tests will need a response from a logged-in user
        self.user = User.objects.get(pk=1)
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)
        
        # POST data to create a game, since multiple tests need this
        self.point_data = [ { 'id' : '0',
                              'lat' : '12.34533',
                              'lon' : '-0.32112' } ]
        self.form_data = { 'game_type' : GAME_TYPES[0][0],
                           'is_public' : True,
                           'city' : 'calgary',
                           'locations' : simplejson.dumps(self.point_data) }

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/create.html')

    def test_context(self):
        check_context(self, ['form', 'gmap_js'])

    def test_game_creation(self):
        # shouldn't be any games yet
        self.assertEqual(Game.objects.count(), 0)
        
        self.response = self.client.post(self.url, self.form_data, follow=True)
        
        # a game should have been created in the database
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.all()[0]
        self.assertEqual(self.form_data['game_type'], game.game_type)
        self.assertEqual(self.form_data['is_public'], game.is_public)
        self.assertEqual(self.form_data['city'], game.city)
        self.assertEqual(self.point_data[0]['lat'], str(game.center_latitude))
        self.assertEqual(self.point_data[0]['lon'], str(game.center_longitude))
        self.assertEqual(self.user, game.created_by)
        
        # we should be redirected to the game editing page
        expUrl = reverse('game_edit', args=(game.id,))
        self.assertRedirects(self.response, expUrl)

    def test_TH_game_creation(self):
        # create a game, and make sure it is a TreasureHunt game
        self.form_data['game_type'] = GAME_TYPES[0][0]
        self.response = self.client.post(self.url, self.form_data, follow=True)
        self.assertTrue(isinstance(Game.objects.all()[0], TreasureHuntGame))
    
    def test_anon_user_redirected(self):
        self.client.logout()
        self.response = self.client.get(self.url)
        expUrl = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(self.response, expUrl)

class TestView_game_details(TestCase):
    url = ''    # actual URL set in setUp()
    view = 'game_details'
    
    def setUp(self):
        create_users(self)
        create_games(self)
        
        # most tests will need a response from a logged-in user,
        # who is NOT the creator of the game
        self.game = Game.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.assertNotEqual(self.user, self.game.created_by)
        self.url = reverse(self.view, args=(self.game.pk,))
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/details.html')

    def test_context(self):
        check_context(self, ['game', 'players', 'can_join_game'])

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

class TestView_game_edit(TestCase):
    url = ''    # actual URL set in setUp()
    view = 'game_edit'
    
    def setUp(self):
        create_users(self)
        create_games(self)
        
        # most tests will need a response from a logged-in user,
        # who is the creator of the game
        self.game = Game.objects.get(pk=1)
        self.user = User.objects.get(pk=1)
        self.assertEqual(self.user, self.game.created_by)
        self.url = reverse(self.view, args=(self.game.pk,))
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/edit.html')

    def test_context(self):
        check_context(
            self,
            ['error_msgs', 'gmap', 'locations'])

    def test_points_correct(self):
        points = utils.locations_to_points(self.game.location_set.all())
        self.assertEqual(self.response.context['gmap'].points,
                         points)

    def test_point_order_correct(self):
        # only applies for TH game currently; thus, the default
        # should be empty
        self.assertEqual(self.response.context['gmap'].point_order, [])
        
        # get the page response for a TH game
        hunt = TreasureHuntGame.objects.all()[0]
        self.assertTrue(isinstance(hunt, TreasureHuntGame))
        self.assertEqual(self.user, hunt.created_by)
        self.url = reverse(self.view, args=(hunt.pk,))
        self.response = self.client.get(self.url)
        
        self.assertEqual(self.response.context['gmap'].point_order,
                         utils.csv_to_list(hunt.ordered_locations))

    def test_add_point(self):
        num_before = self.game.location_set.all().count()
        
        form_data = { 'mode':'add_point' }
        self.response = self.client.post(self.url, form_data)
        self.assertEqual(self.response.status_code, 200)
        
        num_after = self.game.location_set.all().count()
        self.assertEqual(num_before + 1, num_after)
        
        # the new point's location should be the game's center
        new_point = self.game.location_set.all()[num_after - 1]
        self.assertEqual(new_point.latitude, self.game.center_latitude)
        self.assertEqual(new_point.longitude, self.game.center_longitude)

    def test_save_locations(self):
        # change each lat/lon for the game
        old_locations = self.game.location_set.all()[:]
        changed_locations = []

        for old_loc in old_locations:
            changed_locations.append({
                    'id':old_loc.id,
                    'lat':float(old_loc.latitude) * 1.1,
                    'lon':float(old_loc.longitude) * 0.9
                })

        form_data = { 'mode':'update_locations',
                      'locations':simplejson.dumps(changed_locations) }
        self.response = self.client.post(self.url, form_data)
        self.assertEqual(self.response.status_code, 200)
        
        for i, new_loc in enumerate(self.game.location_set.all()):
            old_loc = old_locations[i]
            self.assertAlmostEqual(float(new_loc.latitude),
                                   float(old_loc.latitude) * 1.1)
            self.assertAlmostEqual(float(new_loc.longitude),
                                   float(old_loc.longitude) * 0.9)
            

class TestView_game_QRCodes(TestCase):
    url = ''    # actual URL set in setUp()
    view = 'game_qrcodes'
    
    def setUp(self):
        create_users(self)
        create_games(self)
        
        # most tests will need a response from a logged-in user,
        # who is the creator of the game
        self.game = Game.objects.get(pk=1)
        self.user = User.objects.get(pk=1)
        self.assertEqual(self.user, self.game.created_by)
        self.url = reverse(self.view, args=(self.game.pk,))
        self.assertTrue(
            self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)
        
    def test_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'games/qrcodes.html')
    
    def test_context(self):
        check_context(
            self,
            ['locationQRurls'])
        
    def test_other_user_cannot_view(self):
        #logout current user and log in non-creator
        self.client.logout()
        self.user = User.objects.get(pk=2)
        #check to ensure non-creator cannot view page
        self.assertTrue(
                        self.client.login(username=self.user.username,
                              password=self.user.username))
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 403)

    def test_locations_match_qrurls(self):
        self.assertEqual(self.game.location_set.count(), len(self.response.context['locationQRurls']))
        
    def test_correct_data(self):
        for pair in self.response.context['locationQRurls']:
                self.assertNotEqual(pair[1].find(pair[0].uuid.upper()), -1)
                


class TestGame_TreasureHunt(TestCase):
    
    def setUp(self):
        create_users(self)
        create_games(self)
        
        # create a TreasureHunt game
        self.hunt = TreasureHuntGame()
        self.hunt.created_by = User.objects.get(pk=1)
        self.hunt.save()
    
    def test_saving_location_updates_ordered_locations(self):
        # the TH game's location list should be empty
        self.assertEqual(self.hunt.ordered_locations, '')
        
        # add some locations to the TH game and make
        # sure they get added to ordered_locations
        ids = []
        for i in range(5):
            loc = Location()
            loc.gameID = self.hunt
            loc.save()
            ids.append(loc.id)
        
        game_locs = utils.csv_to_list(self.hunt.ordered_locations)
        for loc_id in ids:
            self.assertTrue(loc_id in game_locs)
        
    def test_treasure_hunt_player_can_only_visit_locations_from_the_game(self):
        # add a location to the TH game
        loc = Location()
        loc.gameID = self.hunt
        loc.save()
        
        # create a TH player
        player = TreasureHuntPlayer()
        player.game = self.hunt
        player.user = User.objects.get(pk=1)
        player.save()
        self.assertTrue(player.highest_visited is None)
        
        # the player has visited the location we added
        player.highest_visited = loc
        player.save()
        self.assertEqual(player.highest_visited, loc)
        
        # attepmt to get the player to visit a location from another game
        other_loc = Location.objects.get(pk=1)
        self.assertNotEqual(other_loc, loc)
        player.highest_visited = other_loc
        self.assertRaises(IntegrityError, player.save)
        
        # the location in the DB should not have changed
        db_player = TreasureHuntPlayer.objects.get(pk=player.id)
        self.assertEqual(db_player.highest_visited, loc)

    def test_game_type_always_correct(self):
        self.assertEqual(self.hunt.game_type, GAME_TYPES[0][0])
        
        # should be filled in if it is blank
        self.hunt.game_type = ''
        self.hunt.save()
        self.assertEqual(self.hunt.game_type, GAME_TYPES[0][0])
        
        # should not allow anything else
        self.hunt.game_type = 'XZ'
        self.assertRaises(IntegrityError, self.hunt.save)


