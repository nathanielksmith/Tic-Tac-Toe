from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from tictactoe.models import *
import re
import time

def index(request, board_id=None):
    if board_id == None:
        name = "Game " + re.sub(r'\d+\.', '', str(time.time()))
        board = Board(name=name)
        board.save()
        return redirect(board)

    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404

    return render_to_response('tictactoe/index.html', {'board':board, 'state':board.state.state})


def move(request, board_id, row, col):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404

    row = int(row)
    col = int(col)

    board.user_move(row, col)
    board.save()
    return redirect(board)
