from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Tutorial/', include('Tutorial.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^polls/', include('qr.polls.urls')),
    
    # test page for Python QR code generation
    (r'^code/(?P<data>.*)$', 'qr.views.qr_code'),
    
    # test page for Google maps API
    (r'^pymap/$', 'qr.views.pymaps_map'),
)
