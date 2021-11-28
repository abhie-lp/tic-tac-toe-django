from django.urls import path
from .views import change_symbol, make_a_move_view, new_game_view

urlpatterns = [
    path("new-game/", new_game_view, name="reset_game"),
    path('make-move/', make_a_move_view, name="make_move"),
    path("change-symbol/", change_symbol, name="change_symbol"),
]
