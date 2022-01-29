from django.urls import path
from .views import change_symbol, make_a_move_view, new_game_with_computer_view, \
    game_with_computer_view, game_with_player_view

urlpatterns = [
    path('with-player/', game_with_player_view, name='player_game'),
    path('with-computer/', game_with_computer_view, name='computer_game'),
    path("new-game/", new_game_with_computer_view, name="reset_game"),
    path('make-move/', make_a_move_view, name="make_move"),
    path("change-symbol/", change_symbol, name="change_symbol"),
    path('with-player/<str:username>', game_with_player_view, name='player_game_user'),
]
