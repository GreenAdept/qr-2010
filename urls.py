from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^polls/', include('qr.polls.urls')),
    
    # test page for Python QR code generation
    #(r'^code/(?P<data>.*)$', 'qr.views.qr_code'),
    
    (r'^$', 'qr.views.index'),
    (r'^login/$', 'qr.views.site_login'),
    (r'^404/$', 'qr.views.er'),
    (r'^registration/$', 'qr.views.registration'),
    (r'^game/', include('qr.games.urls')),
    (r'^profile/$', 'qr.views.profile'),


)



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

