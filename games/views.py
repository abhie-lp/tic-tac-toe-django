from operator import itemgetter
from typing import Optional

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import timeit
from .models import PLAYER_MOVE, Game
from .game import computer_move, Cell, check_winner


@timeit
@login_required()
def change_symbol(request):
    game: Game = request.user.game
    if game.symbol == "X":
        game.symbol = "0"
    else:
        game.symbol = "X"
    game.save()
    return HttpResponse(game.symbol)


@timeit
@login_required()
def game_page(request):
    return render(request, "games/game.html")


@csrf_exempt
@require_POST
@login_required()
@timeit
def make_a_move_view(request):
    game = request.user.game

    row, col = (int(x) for x in itemgetter("row", "col")(request.POST))
    game.board[row][col] = PLAYER_MOVE
    game.save()
    win_status = check_winner(game)
    com_move: Optional[Cell] = None
    if not win_status:
        com_move = computer_move(game)
        win_status = check_winner(game)

    return JsonResponse({"player": game.symbol,
                         "com_position": com_move._asdict()
                         if com_move else None,
                         "win_status": win_status.to_json()
                         if win_status else None})


@timeit
@login_required()
def reset_game_view(request):
    request.user.game.reset_game()
    return redirect("game_page")
