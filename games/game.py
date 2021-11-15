from collections import namedtuple
from typing import Optional

from .models import Game, COMPUTER_MOVE

Cell = namedtuple("Cell", "row col")


def computer_move(game: Game) -> Optional[Cell]:
    """Make a computer move"""
    for row_idx, row in enumerate(game.board):
        for col_idx, col in enumerate(row):
            if col == "-":
                game.board[row_idx][col_idx] = COMPUTER_MOVE
                game.save()
                return Cell(row_idx, col_idx)
