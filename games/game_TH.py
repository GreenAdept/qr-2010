
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from qr.games import utils
from qr.games.models import *

def details(game, player):
    # if the player isn't given, they are not a player in this game;
    # thus return nothing
    if player is None:
        return {}
    
    game_data = {'clue':'', 'complete':False}
    loc_order = utils.csv_to_list(game.ordered_locations)
    
    # if player hasn't visited any locations, give the first clue
    next_index = 0
    if player.highest_visited is not None:
        next_index = 1 + loc_order.index(player.highest_visited.id)
    
    # if player has visited the last location
    if next_index >= len(loc_order):
        game_data['complete'] = True
    else:
        next_location = get_object_or_404(Location, id=loc_order[next_index])
        game_data['clue'] = next_location.clue
    
    return game_data

def process(player, location):
    game_data = {'clue':'', 'complete':False}
    loc_order = utils.csv_to_list(player.game.ordered_locations)
    
    # if the player hasn't visited any locations
    # yet, the next location should be the first one
    next_loc_id = loc_order[0]
    
    if player.highest_visited is not None:
        # if the player has already visited the last location, do nothing
        if player.highest_visited == loc_order[-1]:
            game_data['complete'] = True
            return game_data
        else:
            # otherwise, find the next location the player should be visiting
            next_index = 1 + loc_order.index(player.highest_visited.id)
            next_loc_id = loc_order[next_index]
    
    # if the given location is the one the player should be at next,
    # then advance the player
    if location.id == next_loc_id:
        player.highest_visited = location
        player.save()
    else:
        # the player shouldn't be at this location yet
        raise PermissionDenied('not next location')
    
    # give the player the clue for the location after
    # the one they just told us they visited
    # (unless they're done the game already)
    next_index = 1 + loc_order.index(location.id)
    if next_index >= len(loc_order):
        game_data['complete'] = True
    else:
        next_location = get_object_or_404(Location, id=loc_order[next_index])
        game_data['clue'] = next_location.clue
    
    return game_data

def qrcode(game, location):
    # TODO: Doug: this should return the clue for the
    # location AFTER the given location
    return ''
