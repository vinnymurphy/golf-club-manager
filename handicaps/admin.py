from django.contrib import admin

from .models import Game, GameScore, GameType, Grade, Player

admin.site.register(Player)
admin.site.register(GameType)
admin.site.register(Game)
admin.site.register(GameScore)
admin.site.register(Grade)
