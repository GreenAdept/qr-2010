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
    
    # test page for Google maps API
    (r'^pymap/$', 'qr.views.pymaps_map'),
    (r'^$', 'qr.views.index'),
    (r'^login/$', 'qr.views.sitelogin'),
)



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

