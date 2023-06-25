from django.contrib import admin
from .models import Player, GameType, Game, GameScore, Grade

admin.site.register(Player)
admin.site.register(GameType)
admin.site.register(Game)
admin.site.register(GameScore)
admin.site.register(Grade)
