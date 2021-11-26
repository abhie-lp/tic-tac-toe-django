from django.contrib.admin import ModelAdmin, register
from .models import Game


@register(Game)
class GameAdmin(ModelAdmin):
    list_display = "user", "symbol", "moves_left",
    list_filter = "symbol", "created", "updated",
