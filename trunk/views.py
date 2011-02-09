from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from qr.games.models import *


def index(request):
    num_games = Game.objects.count()
    context = RequestContext(request)
    context['num_games'] = num_games
    return render_to_response('home/index.html', context)
    
def er(request):
    return render_to_response('404.html', RequestContext(request))

def contact(request):    
    return render_to_response('home/contact.html', RequestContext(request))

def site_login(request):
    if request.method == 'GET':
        context = RequestContext(request)
        context['next'] = request.GET['next']
        return render_to_response('home/login.html', context)
    
    if request.method == 'POST':
        redirect_to = None
        try:
            redirect_to = request.POST['next']
            # if the 'next' field is blank, then use the 'path' field
            # (for redirecting back to whatever page the user logged in from)
            if not redirect_to:
                redirect_to = request.POST['path']
        except KeyError:
            pass
        
        # Light security check -- make sure redirect_to isn't garbage.
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = '/'
        
        username = request.POST['UserName']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
               return HttpResponse('Failure')
        else:
            return HttpResponse('Really bad failure')

def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_profile(request, username):
    context = RequestContext(request)
    return render_to_response('users/profile.html', context)
