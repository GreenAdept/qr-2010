from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login
from django.template import Context, Template, RequestContext
import user_management

#import Image
#import thirdparty.PyQRNative as pyqr
#def qr_code(request, data):
#    
#    qr = pyqr.QRCode(2, pyqr.QRErrorCorrectLevel.L)
#    qr.addData(data)
#    qr.make()
#    
#    response = HttpResponse(mimetype='image/png')
#    qr.makeImage().save(response, "PNG")
#    return response


from django.shortcuts import render_to_response
def index(request):    
    if request.method == 'POST':
        login_dict = site_login(request)
        return render_to_response('home/index.html', login_dict)
    else: 
        return render_to_response('home/index.html')
    
def er(request):
        return render_to_response('404.html')
    
def registration(request):
        return render_to_response('users/registration.html')

def site_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return {"user" : user}
        else:
           return render_to_response('Failure')
    else:
        return render_to_response('Really bad failure')
