from django.contrib.admin import ModelAdmin, register
from .models import Game


@register(Game)
class GameAdmin(ModelAdmin):
    list_display = "user", "symbol",
    list_filter = "symbol", "created", "updated",
