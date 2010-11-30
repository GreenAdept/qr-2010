from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'qr.games.views.game_list', name='game_list'),
    url(r'^create/$', 'qr.games.views.game_create', name='game_create'),
    url(r'^(?P<game_id>\d+)/edit/$', 'qr.games.views.game_edit', name='game_edit'),
    url(r'^(?P<game_id>\d+)/$', 'qr.games.views.game_details', name='game_details'),
)
