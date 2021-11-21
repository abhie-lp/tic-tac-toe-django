from collections import namedtuple
from enum import Enum
from typing import Optional, List, Literal

from .models import Game, COMPUTER_MOVE, PLAYER_MOVE

Cell = namedtuple("Cell", "row col")
Line = Literal["row", "col"]


class Diagonal(Enum):
    NONE = None
    FORWARD = "F"
    BACKWARD = "B"


class Winner(Enum):
    NONE = None
    PLAYER = "P"
    COM = "C"


class GameStatus:
    __slots__ = ("row", "col", "diagonal", "winner")

    def __init__(self):
        self.row: Optional[int] = None
        self.col: Optional[int] = None
        self.diagonal: Diagonal = Diagonal.NONE
        self.winner: Winner = Winner.NONE

    def to_json(self):
        return {"row": self.row, "col": self.col,
                "diagonal": self.diagonal.value, "winner": self.winner.value}

    def __str__(self):
        return f'<GameStatus row={self.row} ' \
               f'col={self.col} ' \
               f'diagonal={self.diagonal} ' \
               f'winner={self.winner}>'


def computer_move(game: Game) -> Optional[Cell]:
    """Make a computer move"""
    for row_idx, row in enumerate(game.board):
        for col_idx, col in enumerate(row):
            if col == "-":
                game.board[row_idx][col_idx] = COMPUTER_MOVE
                game.save()
                return Cell(row_idx, col_idx)


def check_line(board: List, line_type: Line) -> Optional[GameStatus]:
    """Check board rows game winner or tie"""
    for idx, line in enumerate(board):
        if len(set(line)) == 1 and line[0] != "-":
            status = GameStatus()
            setattr(status, line_type, idx)
            if line[0] == PLAYER_MOVE:
                status.winner = Winner.PLAYER
            else:
                status.winner = Winner.COM
            return status
    return None


def check_diagonal(board: List) -> Optional[GameStatus]:
    """Check diagonals for the winner or tie"""
    # Get the backward diagonal
    diagonal_bwd = tuple(board[i][i] for i in range(len(board[0])))
    # Get the forward diagonal
    diagonal_fwd = tuple(board[len(board[0]) - 1 - i][i]
                         for i in range(len(board[0]) - 1, -1, -1))

    if len(set(diagonal_fwd)) == 1 and diagonal_fwd[0] != '-':
        status = GameStatus()
        status.diagonal = Diagonal.FORWARD
        if diagonal_fwd[0] == PLAYER_MOVE:
            status.winner = Winner.PLAYER
        else:
            status.winner = Winner.COM
        return status
    elif len(set(diagonal_bwd)) == 1 and diagonal_bwd[0] != '-':
        status = GameStatus()
        status.diagonal = Diagonal.BACKWARD
        if diagonal_bwd[0] == PLAYER_MOVE:
            status.winner = Winner.PLAYER
        else:
            status.winner = Winner.COM
        return status
    return None


def check_winner(game: Game) -> Optional[GameStatus]:
    win_by_row = check_line(game.board, "row")
    if win_by_row:
        return win_by_row

    win_by_col = check_line([[row[i] for row in game.board]
                             for i in range(len(game.board[0]))], "col")
    if win_by_col:
        return win_by_col

    win_by_diagonal = check_diagonal(game.board)
    if win_by_diagonal:
        return win_by_diagonal
    return None
