from django.db.models import Model, OneToOneField, CharField, CASCADE, \
    DateTimeField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model


PLAYER_MOVE = '1'
COMPUTER_MOVE = '2'


def default_board() -> list:
    """Default board for the game"""
    return [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]


class Game(Model):
    user = OneToOneField(get_user_model(),
                         on_delete=CASCADE,
                         related_name="game")
    symbol = CharField(max_length=1, default="X")
    board = ArrayField(ArrayField(
        CharField(max_length=1), size=3
    ), default=default_board, size=3)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def reset_game(self):
        """Reset the board to default state"""
        self.board = default_board()
        self.symbol = "X"
        self.save()
