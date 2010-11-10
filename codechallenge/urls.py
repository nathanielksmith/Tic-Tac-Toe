from django.conf.urls.defaults import *
import tictactoe.views

urlpatterns = patterns('',
    (r'^tictactoe/$', 'tictactoe.views.index'),
    (r'^tictactoe/board/(?P<board_id>\d+)$', 'tictactoe.views.index'),
    (r'^tictactoe/board/(?P<board_id>\d+)/move/(?P<row>\d+)/(?P<col>\d+)$', 'tictactoe.views.move'),
)
