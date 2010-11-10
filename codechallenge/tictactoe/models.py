from django.db import models
from picklefield.fields import PickledObjectField

class GameState():
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]

    def update(self, row, col, piece):
        self.state[row][col] = piece

    def center_row(self):
        return 1

    def center_col(self):
        return 1

    def empty(self, row, col):
        return not bool(self.state[row][col])

class Board(models.Model):
    state  = PickledObjectField(default=GameState())
    name   = models.CharField(default="a tic tac toe game", max_length=50) 
    over   = models.BooleanField()
    status = models.CharField(max_length=20, choices=(('tie', 'Tie'), ('computer', 'I win')))

    def get_absolute_url(self):
        return r'/tictactoe/board/%i' % self.id

    def user_move(self, row, col):
        self.state.update(row, col, 1)
