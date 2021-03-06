from enum import Enum
from random import choice
from typing import Optional, List, Literal, Union

from .models import Cell, Game, EMPTY_MOVE, Winner, GameP2P

Line = Literal["row", "col"]


class Diagonal(Enum):
    NONE = None
    FORWARD = "F"
    BACKWARD = "B"


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


def minimax(game: Game, sign: Winner, is_maximizing: bool) -> int:
    """Player is maximizing and CPU is minimizing"""
    result: GameStatus = check_winner(game)
    if result:
        if result.winner == Winner.TIE:
            return 0
        return (1 if result.winner == Winner.PLAYER1 else -1) * \
               (game.moves_left + 1)
    scores = []
    for cell in game.remaining_moves():
        game = game.make_a_move(cell, sign, commit=False)
        scores.append(minimax(
            game,
            Winner.PLAYER1 if sign == Winner.COMPUTER else Winner.COMPUTER,
            not is_maximizing
        ))
        game.make_a_move(cell, EMPTY_MOVE, commit=False)
    return max(scores) if is_maximizing else min(scores)


def computer_move(game: Game) -> Optional[Cell]:
    """Make a computer move"""
    cell: Cell
    best_move: Cell
    if game.moves_left == 9:
        cell = Cell(choice((0, 1, 2)), choice((0, 1, 2)))
        game.make_a_move(cell, Winner.COMPUTER)
        return cell

    best_score, best_move = float("inf"), Cell(0, 0)
    for cell in game.remaining_moves():
        game: Game = game.make_a_move(cell, Winner.COMPUTER, commit=False)
        score = minimax(game, Winner.PLAYER1, True)
        game.make_a_move(cell, EMPTY_MOVE, commit=False)
        if score < best_score:
            best_score = score
            best_move = cell
    game.make_a_move(best_move, Winner.COMPUTER)
    return best_move


def check_row_and_col(board: List, player1: Winner, player2: Winner) -> Optional[GameStatus]:
    """Check board rows game winner or tie"""
    for row_idx, row in enumerate(board):
        if len(set(row)) == 1 and row[0] != '-':
            status = GameStatus(player1 if row[0] == player1 else player2)
            status.row = row_idx
            return status

    no_empty_cell = True
    # Check for col
    transpose_board = [[row[i] for row in board] for i in range(len(board[0]))]
    for col_idx, col in enumerate(transpose_board):
        if len(set(col)) == 1 and col[0] != "-":
            status = GameStatus(player1 if col[0] == player1 else player2)
            status.col = col_idx
            return status
        # Check if any value in col is -
        if no_empty_cell:
            if '-' in col:
                no_empty_cell = False

    # If there are no empty cells return Result as draw
    if no_empty_cell:
        return GameStatus(Winner.TIE)
    return None


def _diagonal_winner(values: tuple) -> bool:
    if len(set(values)) == 1 and values[0] != '-':
        return True
    return False


def check_diagonal(board: List, player1: Winner, player2: Winner) -> Optional[GameStatus]:
    """Check diagonals for the winner or tie"""
    # Get the forward diagonal
    diagonal_fwd = tuple(board[i][i] for i in range(len(board[0])))
    if _diagonal_winner(diagonal_fwd):
        status = GameStatus(player1 if diagonal_fwd[0] == player1 else player2)
        status.diagonal = Diagonal.FORWARD
        return status

    # Get the backward diagonal
    diagonal_bwd = tuple(board[len(board[0]) - 1 - i][i]
                         for i in range(len(board[0]) - 1, -1, -1))
    if _diagonal_winner(diagonal_bwd):
        status = GameStatus(player1 if diagonal_bwd[0] == player1 else player2)
        status.diagonal = Diagonal.BACKWARD
        return status
    return None


def check_winner(
        game: Union[Game, GameP2P],
        player1: Winner = Winner.PLAYER1,
        player2: Winner = Winner.COMPUTER
) -> Optional[GameStatus]:
    if game.moves_left < 5:
        result: GameStatus = check_row_and_col(game.board, player1, player2)
        if result:
            return result
        result: GameStatus = check_diagonal(game.board, player1, player2)
        if result:
            return result
    return None
