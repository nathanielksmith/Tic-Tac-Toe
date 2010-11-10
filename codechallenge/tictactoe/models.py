from django.db import models
from picklefield.fields import PickledObjectField

class GameState():
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]

class Board(models.Model):
    state = PickledObjectField(default=GameState())
    name  = models.CharField(default="I must break you.", max_length=50) 

    def get_absolute_url(self):
        return r'/tictactoe/board/%i' % self.id

    def user_move(row, col):
        pass
