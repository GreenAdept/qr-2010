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


import thirdparty.pymaps as pymaps
def pymaps_map(request):
    
    map_obj = pymaps.PyMap()
    map_obj.maps[0].center = (51.270373,-113.98766)
    map_obj.maps[0].zoom = "15"
    
    icon2 = pymaps.Icon('icon2')               # create an additional icon
    icon2.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
    icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
    map_obj.addicon(icon2)
    
    map_obj.maps[0].setpoint([51.270373,-113.98766, 'Dougs house!', 'icon2'])
    
    return HttpResponse(map_obj.showhtml())

from django.shortcuts import render_to_response

def index(request):
        return render_to_response('home/index.html')
    
def er(request):
        return render_to_response('404.html')

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
