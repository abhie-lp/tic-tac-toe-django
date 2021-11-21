from operator import itemgetter
from typing import Optional

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import PLAYER_MOVE
from .game import computer_move, Cell, check_winner


@login_required()
def change_symbol(request):
    symbol = request.user.game.symbol
    if symbol == "X":
        symbol = "0"
    else:
        symbol = "X"
    request.user.game.symbol = symbol
    request.user.game.save()
    return HttpResponse(symbol)


@login_required()
def game_page(request):
    return render(request, "games/game.html")


@csrf_exempt
@require_POST
@login_required()
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


@login_required()
def reset_game_view(request):
    request.user.game.reset_game()
    return redirect("game_page")
