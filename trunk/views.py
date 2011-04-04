from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from qr.games.models import Game as Game
from qr.games.models import ActivityStreamItem as ActivityStream
from django import template
from django.contrib.auth.models import User
import datetime


def index(request):
    context = RequestContext(request)
    context = page_info(context)
    
    return render_to_response('home/index.html', context)
    
def er(request):
	context = RequestContext(request)
	context = page_info(context)
	return render_to_response('404.html', context)

def contact(request):
	context = RequestContext(request)   
	context = page_info(context) 
	return render_to_response('home/contact.html', context)

def site_login(request):
    if request.method == 'GET':
        context = RequestContext(request)
        context['next'] = request.GET['next']
        context = page_info(context)
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
    context = page_info(context) 
    return render_to_response('users/profile.html', context)
    
    
def page_info(context):
	num_games = Game.objects.count()
	context['num_games'] = num_games
	activity_stream = ActivityStream.objects.all()
	context['activity_stream'] = activity_stream
	context['num_users'] = online_users()
	return context
	
def online_users():
    """
    Show user that has been login an hour ago.
    """
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    sql_datetime = datetime.datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    users = User.objects.filter(last_login__gt=sql_datetime,
                                is_active__exact=1).order_by('-last_login')
    return users.count()
