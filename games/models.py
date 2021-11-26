from collections import namedtuple
from typing import List

from django.db.models import Model, OneToOneField, CharField, CASCADE, \
    DateTimeField, PositiveSmallIntegerField
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

PLAYER_MOVE = '1'
COMPUTER_MOVE = '2'
EMPTY_MOVE = '-'
Cell = namedtuple("Cell", "row col")


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
    moves_left = PositiveSmallIntegerField(default=9)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def make_a_move(
            self, cell: Cell, sign: str, commit: bool = True
    ) -> "Game":
        """
        Make Player or Computer move and decrement the moves_left if commit
        """
        self.board[cell.row][cell.col] = sign
        if commit:
            self.moves_left -= 1
            self.save()
        return self

    def reset_game(self):
        """Reset the board to default state"""
        self.board = default_board()
        self.symbol = "X"
        self.moves_left = 9
        self.save()

    def remaining_moves(self) -> List[Cell]:
        """Return a list of all remaining moves"""
        moves = []
        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if col == EMPTY_MOVE:
                    moves.append(Cell(row_idx, col_idx))
        return moves
