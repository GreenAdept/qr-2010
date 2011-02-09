from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext


def registration(request):   
    if (request.method == 'POST'):
        user = User.objects.create_user(request.POST['UserName'], request.POST['Email'], request.POST['Password'])
        user = authenticate(username=request.POST['UserName'], password=request.POST['Password'])
        login(request, user)
        user.profile.firstname = request.POST['FirstName']
        user.get_profile().firstname = request.POST['FirstName']
        user.get_profile().lastname = request.POST['LastName']
        user.get_profile().save()
        context = RequestContext(request)
        context['Success'] = True
        # Check the validity of what they've entered
        context['UserName'] = request.POST['UserName']
        context['FirstName'] = request.POST['FirstName']
        context['LastName'] = request.POST['LastName']
        context['Email'] = request.POST['Email']

        return render_to_response('users/registration.html', context)
    else:
        return render_to_response('users/registration.html')