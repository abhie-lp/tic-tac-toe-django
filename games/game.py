from enum import Enum
from random import choice
from typing import Optional, List, Literal

from .models import Cell, Game, COMPUTER_MOVE, PLAYER_MOVE, EMPTY_MOVE


Line = Literal["row", "col"]


class Diagonal(Enum):
    NONE = None
    FORWARD = "F"
    BACKWARD = "B"


class Winner(Enum):
    NONE = None
    PLAYER = "P"
    COM = "C"
    TIE = "T"


class GameStatus:
    __slots__ = ("row", "col", "diagonal", "winner")

    def __init__(self, winner: Winner = Winner.NONE):
        self.row: Optional[int] = None
        self.col: Optional[int] = None
        self.diagonal: Diagonal = Diagonal.NONE
        self.winner: Winner = winner

    def to_json(self):
        return {"row": self.row, "col": self.col,
                "diagonal": self.diagonal.value, "winner": self.winner.value}

    def __str__(self):
        return f'<GameStatus row={self.row} ' \
               f'col={self.col} ' \
               f'diagonal={self.diagonal} ' \
               f'winner={self.winner}>'


def minimax(game: Game, sign: str, is_maximizing: bool) -> int:
    """Player is maximizing and CPU is minimizing"""
    result: GameStatus = check_winner(game)
    if result:
        if result.winner == Winner.TIE:
            return 0
        return 1 if result.winner == Winner.PLAYER else -1
    scores = []
    for cell in game.remaining_moves():
        game = game.make_a_move(cell, sign, commit=False)
        scores.append(minimax(
            game,
            PLAYER_MOVE if sign == COMPUTER_MOVE else COMPUTER_MOVE,
            not is_maximizing
        ))
        game.make_a_move(cell, EMPTY_MOVE, commit=False)
    return max(scores) if is_maximizing else min(scores)


def computer_move(game: Game) -> Optional[Cell]:
    """Make a computer move"""
    cell: Cell
    best_move: Cell
    if game.moves_left == 9:
        cell = Cell(choice((1, 2, 3)), choice((1, 2, 3)))
        game.make_a_move(cell.row, cell.col, COMPUTER_MOVE)
        return cell

    best_score, best_move = float("inf"), Cell(0, 0)
    for cell in game.remaining_moves():
        game: Game = game.make_a_move(cell, COMPUTER_MOVE, commit=False)
        score = minimax(game, PLAYER_MOVE, True)
        game.make_a_move(cell, EMPTY_MOVE, commit=False)
        if score < best_score:
            best_score = score
            best_move = cell
    game.make_a_move(best_move, COMPUTER_MOVE)
    return best_move


def check_line(board: List, line_type: Line) -> Optional[GameStatus]:
    """Check board rows game winner or tie"""
    no_empty_cell = True
    for idx, line in enumerate(board):
        if len(set(line)) == 1 and line[0] != "-":
            status = GameStatus()
            setattr(status, line_type, idx)
            if line[0] == PLAYER_MOVE:
                status.winner = Winner.PLAYER
            else:
                status.winner = Winner.COM
            return status
        if no_empty_cell:
            for cell in line:
                if cell == "-":
                    no_empty_cell = False
    if no_empty_cell:
        return GameStatus(winner=Winner.TIE)
    return None


def _diagonal_winner(values: tuple) -> Optional[GameStatus]:
    if len(set(values)) == 1 and values[0] != '-':
        status = GameStatus(
            Winner.PLAYER if values[0] == PLAYER_MOVE else Winner.COM
        )
        status.diagonal = Diagonal.FORWARD
        return status
    return None


def check_diagonal(board: List) -> Optional[GameStatus]:
    """Check diagonals for the winner or tie"""
    # Get the forward diagonal
    diagonal_fwd = tuple(board[len(board[0]) - 1 - i][i]
                         for i in range(len(board[0]) - 1, -1, -1))
    result: GameStatus = _diagonal_winner(diagonal_fwd)

    if result:
        return result

    # Get the backward diagonal
    diagonal_bwd = tuple(board[i][i] for i in range(len(board[0])))
    result: GameStatus = _diagonal_winner(diagonal_bwd)
    if result:
        return result
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
