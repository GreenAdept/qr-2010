from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext

def qr_create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    User.objects.create_user(username, password)
    
def registration(request):   
    if (request.method == 'POST'):
        user = User.objects.create_user(request.POST['UserName'], request.POST['Email'], request.POST['Password'])
        user = authenticate(username=request.POST['UserName'], password=request.POST['Password'])
        login(request, user)
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