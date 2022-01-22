from django.contrib.admin import ModelAdmin, register
from .models import Game, GameP2P


@register(Game)
class GameAdmin(ModelAdmin):
    list_display = "user", "symbol", "moves_left", "winner"
    list_filter = "symbol", "created", "updated", "winner"


@register(GameP2P)
class GameP2PAdmin(ModelAdmin):
    list_display = 'player1', 'player2', 'winner', 'player1_symbol', \
                   'player2_symbol', 'player1_wins', 'player2_wins', \
                   'moves_left', 'total_games'
    list_filter = 'player1_symbol', 'player2_symbol', 'created', 'updated'
