from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'qr.games.views.game_list'),
    (r'^create/$', 'qr.games.views.create'),
    url(r'^(?P<game_id>\d+)/$', 'qr.games.views.location_pick', name='location_pick'),
)
