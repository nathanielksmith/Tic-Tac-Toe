from django.conf.urls.defaults import *
import tictactoe.views

urlpatterns = patterns('',
    # load a board
    (r'^tictactoe/$', 'tictactoe.views.index'),
    (r'^tictactoe/board/(?P<board_id>\d+)$', 'tictactoe.views.index'),
    # make a move. Redirects to board with updated game state.
    (r'^tictactoe/board/(?P<board_id>\d+)/move/(?P<row>\d+)/(?P<col>\d+)$', 'tictactoe.views.move'),
)
