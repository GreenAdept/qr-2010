from django.http import HttpResponse
from django.contrib.auth import authenticate, login

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
        return render_to_response('home/index.html')
    
def er(request):
        return render_to_response('404.html')
    
def createUser(request):
        return render_to_response('users/createUser.html')

def sitelogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('home/logged-in.html')
        #else:
         #   return render_to_response('Failure')
    else:
        return render_to_response('Really bad failure')
