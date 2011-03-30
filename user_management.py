from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from forms import UserRegistrationForm
import datetime
import Image


def registration(request):   
    if request.method == 'POST': # If the form has been submitted...
        form = UserRegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            if request.user.is_authenticated():
                user = User.objects.get(username__exact=request.user.username)
                if(user.check_password(form.cleaned_data['passw'])):
                    if(form.cleaned_data['year'] != None) and (form.cleaned_data['month'] != None) and (form.cleaned_data['day'] != None):
                            try:
                                user.get_profile().birthday = datetime.date(int(form.cleaned_data['year']), int(form.cleaned_data['month']), int(form.cleaned_data['day']))
                            except:
                                pass
                    if(form.cleaned_data['bio'] != None): 
                            user.get_profile().bio = form.cleaned_data['bio']          
                    if 'photo' in request.FILES:
                            user.get_profile().photo = request.FILES['photo']
                            im = Image.open(user.get_profile().photo)
                    else:
                        user.get_profile().photo = 'media/unknown_user.gif'
                    if(form.cleaned_data['gender'] != None): 
                            user.get_profile().gender = form.cleaned_data['gender']   
                    if(form.cleaned_data['firstname'] != None):
                            user.get_profile().firstname = form.cleaned_data['firstname']
                    if(form.cleaned_data['lastname'] != None):
                            user.get_profile().lastname = form.cleaned_data['lastname']
                    if(form.cleaned_data['uemail'] != None):
                            user.email = form.cleaned_data['uemail']
                    user.get_profile().save()
                    context = RequestContext(request)
                    return render_to_response('users/profile.html', context)
        
            if not request.user.is_authenticated():
                    #First initialize a basic user
                    user = User.objects.create_user(form.cleaned_data['usern'], form.cleaned_data['uemail'], form.cleaned_data['passw'])
                    user = authenticate(username=form.cleaned_data['usern'], password=form.cleaned_data['passw'])
                    login(request, user)
                   
                    #Set up extended user profile
                    user.profile.firstname = form.cleaned_data['firstname']
                    user.get_profile().firstname = request.POST['firstname']
                    user.get_profile().lastname = request.POST['lastname']
                    
                    if 'photo' in request.FILES:
                        user.get_profile().photo = request.FILES['photo']
                        im = Image.open(user.get_profile().photo)
                    else:
                        user.get_profile().photo = 'media/unknown_user.gif'
                        
                    user.get_profile().gender = form.cleaned_data['gender']
                    print form.cleaned_data['year']
                    print form.cleaned_data['month']
                    print form.cleaned_data['day']
                    if((form.cleaned_data['year'] is not '') and (form.cleaned_data['month'] is not '') and (form.cleaned_data['day'] is not '')):
                            try:
                                user.get_profile().birthday = datetime.date(int(form.cleaned_data['year']), int(form.cleaned_data['month']), int(form.cleaned_data['day']))
                            except:
                                pass
                    user.get_profile().bio = request.POST['bio']
                    user.get_profile().save()
                        
                    #Set up context
                    context = RequestContext(request)
                    context['Success'] = True
                    context['UserName'] = form.cleaned_data['usern']
                    context['FirstName'] = form.cleaned_data['firstname']
                    context['LastName'] = form.cleaned_data['lastname']
                    context['Email'] =form.cleaned_data['uemail']
                    context['Bio']= form.cleaned_data['bio']
                    context['Gender']= form.cleaned_data['gender']
                    context['Birthday']= user.get_profile().birthday
                    context['Photo'] = user.get_profile().photo
                    return render_to_response('users/registration.html', context)
            else:
                    context = RequestContext(request) 
                    context['form'] = form 
        else:
            context = RequestContext(request) 
            context['form'] = form 
                
     # Populate the form if the user is logged in
    elif request.user.is_authenticated():
        user = request.user
        form = UserRegistrationForm(initial={'usern': user.username,
                                             'firstname':user.get_profile().firstname ,
                                             'lastname': user.get_profile().lastname,
                                             'uemail': user.email,
                                             'gender': user.get_profile().gender,
                                             'birthday': user.get_profile().birthday,
                                             'bio': user.get_profile().bio,
                                             'photo': user.get_profile().photo,
                                             'passw': user.password,
                                             'passwr': user.password,})    
        context = RequestContext(request) 
        context['form'] = form 
          
    else:
        form = UserRegistrationForm()
        context = RequestContext(request) 
        context['form'] = form 
    
    return render_to_response('users/registration.html', context)

