
from django.contrib.auth.models import User
from qr.games.models import *

from datetime import datetime

def create_games(testcase):
    # the first two games should not be of any specific type
    games = [
        { 'type':'XX', 'pub':True, 'city':'UofC',
            'center':[51, -114], 'user':1,
            'locs':[ [51, -114], [51.07, -114.08], [51.07, -114.07] ] },
        { 'type':'XX', 'pub':False, 'city':'Calgary',
            'center':[52, -114], 'user':2,
            'locs':[ [51.079, -114.13], [51.0789, -114.01] ] },
        { 'type':'TH', 'pub':True, 'city':'UofC',
            'center':[52, -114], 'user':1,
            'locs':[ [51.079, -114.13], [51.0789, -114.01] ] },
    ]
    
    for game_info in games:
        game = None
        if game_info['type'] == GAME_TYPES[0][0]:
            game = TreasureHuntGame()
        else:
            game = Game()
        game.game_type = game_info['type']
        game.is_public = game_info['pub']
        game.city = game_info['city']
        game.center_latitude = game_info['center'][0]
        game.center_longitude = game_info['center'][1]
        game.created_by = User.objects.get(pk=game_info['user'])
        game.created = datetime.now()
        game.save()
        
        for loc_info in game_info['locs']:
            loc = Location()
            loc.latitude = str(loc_info[0])
            loc.longitude = str(loc_info[1])
            loc.gameID = game
            loc.created = datetime.now()
            loc.visible = datetime.now()
            loc.expires = datetime.now()
            loc.save()
        
        testcase.assertEqual(game.location_set.count(), len(game_info['locs']))
    
    testcase.assertEqual(Game.objects.all().count(), len(games))

