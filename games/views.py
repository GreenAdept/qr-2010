# Create your views here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.utils import simplejson

from qr.games.gmap import Map
from qr.games.models import Game, Location, PartialGameForm

def game_list(request):
    games = Game.objects.all()
    
    context = RequestContext(request)
    context['game_list'] = games
    return render_to_response('games/list.html', context)

@login_required(redirect_field_name='home/index.html')
def create(request):
    if request.method == 'POST':
        form = PartialGameForm(request.POST)
        if form.is_valid():
            center_loc = simplejson.loads(request.POST['locations'])[0]
            
            game = form.save(commit=False)
            game.center_latitude = str(center_loc['lat'])
            game.center_longitude = str(center_loc['lon'])
            game.created_by = User.objects.all()[0] # HACK - should be the currently logged in user
            game.created = datetime.now()
            game.save()
            
            return HttpResponseRedirect(reverse('location_pick', args=(game.id,)))

    else:
        form = PartialGameForm()

    gmap = Map('gmap', [(0,0,0,'')])
    gmap.center = (0,0)
    gmap.zoom = '3'
    
    context = RequestContext(request)
    context['form'] = form
    context['gmap_js'] = gmap.to_js()
    return render_to_response('games/create.html', context)

def location_pick(request, game_id):
    
    # get the game
    game = get_object_or_404(Game, pk=game_id)
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
            
            # re-load the locations to grab any added ones
            locations = game.location_set.all()
    
    # convert Locations into points for the map
    points = []
    for loc in locations:
        points.append((str(loc.id),
                       str(loc.latitude),
                       str(loc.longitude),
                       str(loc.clue),))
    
    gmap = Map('gmap', points)
    gmap.center = (game.center_latitude, game.center_longitude)
    gmap.zoom = '15'
    
    context = RequestContext(request)
    context['error_msgs'] = error_msgs
    context['gmap_js'] = gmap.to_js()
    context['created_by_user'] = (request.user == game.created_by)
    return render_to_response('games/location_pick.html', context)


