from operator import itemgetter

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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
    if game.symbol == "X":
        move = 1
    else:
        move = 2

    row, col = (int(x) for x in itemgetter("row", "col")(request.POST))
    game.board[row][col] = move
    game.save()
    return HttpResponse(
        f"<button class='square white'>{game.symbol}</button>"
    )
