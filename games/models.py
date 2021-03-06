from collections import namedtuple
from typing import List, TypeVar

from django.db.models import Model, OneToOneField, CharField, CASCADE, \
    DateTimeField, PositiveSmallIntegerField, TextChoices, ForeignKey
from django.db.models.manager import Manager
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

from accounts.models import CustomUser
from .managers import GameP2PManager


class Winner(TextChoices):
    NONE = ""
    PLAYER1 = "A"
    PLAYER2 = "B"
    COMPUTER = 'C'
    TIE = "T"


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
            self.save(update_fields=('board', 'moves_left'))
        return self

    def new_game(self, commit: bool = True):
        """Reset the board to default state"""
        self.board = default_board()
        self.moves_left = TOTAL_MOVES
        self.winner = None
        if commit:
            self.save()

    def remaining_moves(self) -> List[Cell]:
        """Return a list of all remaining moves"""
        moves = []
        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if col == EMPTY_MOVE:
                    moves.append(Cell(row_idx, col_idx))
        return moves

    def save_winner(self, winner: Winner, commit: bool = True):
        """Set winner field"""
        self.winner = winner.value
        if commit:
            self.save(update_fields=('winner',))

    def change_symbol(self) -> T:
        """Change the current symbol"""
        if self.symbol == "X":
            self.symbol = "0"
        else:
            self.symbol = "X"
        self.save(update_fields=('symbol',))
        return self


class Game(GameAbstract):
    user: CustomUser = OneToOneField(
        get_user_model(), on_delete=CASCADE, related_name="game"
    )
    symbol = CharField(max_length=1, default="X")

    def __str__(self):
        return self.user.username


class GameP2P(GameAbstract):
    player1: CustomUser = ForeignKey(
        get_user_model(), on_delete=CASCADE,
        related_name='player1', db_index=True
    )
    player2: CustomUser = ForeignKey(
        get_user_model(), on_delete=CASCADE,
        related_name='player2', db_index=True
    )
    player1_symbol = CharField(max_length=1, default='X')
    player2_symbol = CharField(max_length=1, default='O')
    player1_wins = PositiveSmallIntegerField(default=0)
    player2_wins = PositiveSmallIntegerField(default=0)
    total_games = PositiveSmallIntegerField(default=0)

    objects = Manager()
    game = GameP2PManager()

    class Meta:
        unique_together = ('player1', 'player2')

    def __str__(self):
        return f'{self.player1.username} V {self.player2.username}'

    def new_game(self, commit: bool = True):
        super(GameP2P, self).new_game(commit=False)
        self.total_games += 1
        if commit:
            self.save(update_fields=('board', 'total_games', 'winner', 'moves_left'))

    def save_winner(self, winner: Winner, commit: bool = True):
        update_fields = ['winner']
        self.winner = winner
        if winner == Winner.PLAYER1:
            self.player1_wins += 1
            update_fields.append('player1_wins')
        elif winner == Winner.PLAYER2:
            self.player2_wins += 1
            update_fields.append('player2_wins')
        if commit:
            self.save(update_fields=update_fields)

    def make_a_move(self, cell: Cell, sign: Winner, commit: bool = True) -> 'GameP2P':
        self.refresh_from_db(fields=('board', 'moves_left'))
        return super(GameP2P, self).make_a_move(cell, sign, commit)

    def change_symbol(self) -> 'GameP2P':
        if self.player1_symbol == 'X':
            self.player1_symbol, self.player2_symbol = 'O', 'X'
        else:
            self.player1_symbol, self.player2_symbol = 'X', 'O'
        self.save(update_fields=('player1_symbol', 'player2_symbol'))
        return self
