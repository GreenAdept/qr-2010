
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson

from qr.games.gmap import Map
from qr.games.models import *
from qr.games import utils

from thirdparty.pygooglechart import QRChart

def game_list(request):
    games = Game.objects.all()
    
    context = RequestContext(request)
    context['game_list'] = games
    return render_to_response('games/list.html', context)

def game_details(request, game_id):
    
    # get the game & its players
    game = get_object_or_404(Game, pk=game_id)
    players = game.player_set.all()
    
    # see if the current user is a player
    cur_player = players.filter(user__exact=request.user)
    
    # the user wants to join the game
    if request.method == 'POST':
        if request.POST['mode'] == 'join':
            # only join if the player isn't already in the game
            if cur_player.count() == 0:
                player = Player(game=game, user=request.user)
                player.save()
    
    can_join_game = False
    if request.user.is_authenticated():
        # the user can join the game if they didn't create it
        # and they aren't already in the game
        if request.user != game.created_by:
            can_join_game = (cur_player.count() == 0)
    
    context = RequestContext(request)
    context['game'] = game
    context['players'] = players
    context['can_join_game'] = can_join_game
    return render_to_response('games/details.html', context)

@login_required
def game_create(request):
    if request.method == 'POST':
        form = PartialGameForm(request.POST)
        if form.is_valid():
            center_loc = simplejson.loads(request.POST['locations'])[0]
            
            data = form.cleaned_data
            game = None
            if data['game_type'] == GAME_TYPES[0][0]:
                game = TreasureHuntGame()
            else:
                # this generic case shouldn't normally occur
                game = Game()
            
            game.is_public = data['is_public']
            game.city = data['city']
            game.center_latitude = str(center_loc['lat'])
            game.center_longitude = str(center_loc['lon'])
            game.created_by = request.user
            game.created = datetime.now()
            game.save()
            
            return HttpResponseRedirect(reverse('game_edit', args=(game.id,)))

    else:
        form = PartialGameForm()

    gmap = Map('gmap', [(0,0,0,'')])
    gmap.center = (0,0)
    gmap.zoom = '3'
    
    context = RequestContext(request)
    context['form'] = form
    context['gmap_js'] = gmap.to_js()
    return render_to_response('games/create.html', context)

@login_required
def game_edit(request, game_id):
    
    # get the game
    game = get_object_or_404(Game, pk=game_id)
    
    # only the game's creator can edit the locations
    if request.user != game.created_by:
        return HttpResponseForbidden('Cannot access: not game creator')
    
    locations = game.location_set.all()
    
    error_msgs = []
    if request.method == 'POST':
        # save locations, if they were given
        if request.POST['mode'] == 'update_locations':
            new_locations = simplejson.loads(request.POST['locations'])
            
            for loc in new_locations:
                # make sure this location ID exists & is
                # linked with the current game_id
                try:
                    existing_loc = locations.get(pk=loc['id'])
                except ObjectDoesNotExist:
                    error_msgs.append(
                        'location[%d] not linked to game[%d]'
                        % (int(loc['id']), int(game_id)))
                
                # set the new lat/lon
                existing_loc.latitude = str(loc['lat'])
                existing_loc.longitude = str(loc['lon'])
                
                # save any game-specific data (from the edit_XX.html templates)
                if isinstance(game, TreasureHuntGame):
                    existing_loc.clue = request.POST['clue_%d' % (existing_loc.id,)]
                
                existing_loc.save()

        # add a new point
        elif request.POST['mode'] == 'add_point':
            new_loc = Location(latitude=game.center_latitude,
                               longitude=game.center_longitude,
                               created=datetime.now(),
                               visible=datetime.now(),
                               expires=datetime.now(),
                               gameID=game)
            new_loc.save()
            
            # re-load the locations to grab the new point
            locations = game.location_set.all()
    
    # if this is a game with an ordering to the points,
    # grab that order for the map to connect the points
    point_order = []
    if isinstance(game, TreasureHuntGame):
        point_order = utils.csv_to_list(game.ordered_locations)
    
    points = utils.locations_to_points(locations)
    gmap = Map('gmap', points, point_order)
    gmap.center = (game.center_latitude, game.center_longitude)
    gmap.zoom = '15'
    
    context = RequestContext(request)
    context['gmap'] = gmap
    context['error_msgs'] = error_msgs
    context['game'] = game
    context['locations'] = locations
    return render_to_response('games/edit.html', context)


def game_qrcodes(request, game_id):
    # get the game
    game = get_object_or_404(Game, pk=game_id)
    
    # only the game's creator can print the clues
    if request.user != game.created_by:
        return HttpResponseForbidden('Cannot access: not game creator')
    
    # get locations and clues
    locations = game.location_set.all()
    
    locationQRurls = []
    
    
    for loc in locations:
        #create chart
        chart = QRChart(200,200)
        
        #add data
        chart.add_data(loc.uuid.upper())
        
        #add the url to QRurls
        locationQRurls.append( (loc, chart.get_url()))
        

    context = RequestContext(request)
    context['locationQRurls'] = locationQRurls
    return render_to_response('games/qrcodes.html', context)
