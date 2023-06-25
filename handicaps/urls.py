from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.player_list, name="player_list"),
    re_path(r"^inactive_players/", views.inactive_players, name="inactive_players"),
    re_path(r"^game/", views.game, name="game"),
    re_path(r"^settings/", views.settings, name="settings"),
    re_path(r"^new_game_type/", views.new_game_type, name="new_game_type"),
    re_path(r"^new_player/", views.new_player, name="new_player"),
    re_path(
        r"^edit_player/(?P<pk>[0-9]+)/edit$",
        views.edit_player,
        name="edit_player",
    ),
    re_path(r"^game_list/", views.game_list, name="game_list"),
    re_path(
        r"^expand_game/(?P<pk>[0-9]+)", views.expand_game, name="expand_game"
    ),
    re_path(
        r"^edit_game_type/(?P<pk>[0-9]+)/edit$",
        views.edit_game_type,
        name="edit_game_type",
    ),
    re_path(r"^grade/", views.grade, name="grade"),
    re_path(r"^config_grade/", views.config_grade, name="config_grade"),
    re_path(
        r"^expand_player/(?P<pk>[0-9]+)/",
        views.expand_player,
        name="expand_player",
    ),
    re_path(
        r"^edit_gamescore/(?P<pk>[0-9]+)/edit$",
        views.edit_gamescore,
        name="edit_gamescore",
    ),
    re_path(r"^attendance/", views.attendance, name="attendance"),
    re_path(r"^stableford/", views.stableford, name="stableford"),
    re_path(
        r"^update_game/(?P<pk>[0-9]+)/", views.update_game, name="update_game"
    ),
    re_path(
        r"^delete_game/(?P<pk>[0-9]+)/", views.delete_game, name="delete_game"
    ),
]
