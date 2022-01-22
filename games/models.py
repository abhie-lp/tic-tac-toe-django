from collections import namedtuple
from typing import List, TypeVar

from django.db.models import Model, OneToOneField, CharField, CASCADE, \
    DateTimeField, PositiveSmallIntegerField, TextChoices
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class Winner(TextChoices):
    NONE = ""
    PLAYER1 = "P"
    PLAYER2 = "C"
    TIE = "T"


PLAYER1_MOVE = Winner.PLAYER1
COMPUTER_MOVE = Winner.PLAYER2
PLAYER2_MOVE = Winner.PLAYER2
EMPTY_MOVE = '-'
TOTAL_MOVES = 9
Cell = namedtuple("Cell", "row col")


def default_board() -> list:
    """Default board for the game"""
    return [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]


T = TypeVar('T', bound='GameAbstract')


class GameAbstract(Model):
    board = ArrayField(ArrayField(
        CharField(max_length=1), size=3
    ), default=default_board, size=3)
    moves_left = PositiveSmallIntegerField(default=TOTAL_MOVES)
    winner = CharField(choices=Winner.choices, max_length=1,
                       null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def make_a_move(
            self, cell: Cell, sign: Winner, commit: bool = True
    ) -> T:
        """
        Make Player or Computer move and decrement the moves_left if commit
        """
        self.board[cell.row][cell.col] = sign
        # Decrement sign if move is other than EMPTY_MOVE else increase
        self.moves_left -= 1 if sign != EMPTY_MOVE else -1
        if commit:
            self.save()
        return self

    def new_game(self):
        """Reset the board to default state"""
        self.board = default_board()
        self.moves_left = TOTAL_MOVES
        self.winner = None
        self.save()

    def remaining_moves(self) -> List[Cell]:
        """Return a list of all remaining moves"""
        moves = []
        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if col == EMPTY_MOVE:
                    moves.append(Cell(row_idx, col_idx))
        return moves


class Game(GameAbstract):
    user: CustomUser = OneToOneField(
        get_user_model(), on_delete=CASCADE, related_name="game"
    )
    symbol = CharField(max_length=1, default="X")

    def __str__(self):
        return self.user.username
