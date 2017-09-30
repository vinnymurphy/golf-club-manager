from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.player_list, name='player_list'),
    url(r'^inactive_players/', views.inactive_players, name='inactive_players'),
    url(r'^game/', views.game, name='game'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^new_game_type/', views.new_game_type, name='new_game_type'),
    url(r'^new_player/', views.new_player, name='new_player'),
    url(r'^edit_player/(?P<pk>[0-9]+)/edit$', views.edit_player, name='edit_player'),
    url(r'^game_list/', views.game_list, name='game_list'),
    url(r'^edit_game_type/(?P<pk>[0-9]+)/edit$', views.edit_game_type, name='edit_game_type'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^config_grade/', views.config_grade, name='config_grade'),
    url(r'^expand_player/(?P<pk>[0-9]+)/', views.expand_player, name='expand_player'),
    url(r'^edit_gamescore/(?P<pk>[0-9]+)/edit$', views.edit_gamescore, name='edit_gamescore'),
    url(r'^attendance/', views.attendance, name='attendance'),
    ]
