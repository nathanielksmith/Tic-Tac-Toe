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

    def first_free(self):
        r,c = (0,0)
        for row in self.state:
            for col in row:
                if self.empty(r,c):
                    return (r,c)
                c += 1
            r += 1
    
    def two_in_a_row(self, piece):
        return (None, None)

class Board(models.Model):
    state  = PickledObjectField(default=GameState())
    name   = models.CharField(default="a tic tac toe game", max_length=50) 
    over   = models.BooleanField()
    status = models.CharField(max_length=20, choices=(('tie', 'Tie'), ('computer', 'I win')))

    def get_absolute_url(self):
        return r'/tictactoe/board/%i' % self.id

    def user_move(self, user_row, user_col):
        if not self.state.empty(user_row,user_col):
            return

        self.state.update(user_row, user_col, 1)

        # Can I win?
        row, col = self.state.two_in_a_row(2)

        if row is not None and col is not None:
            self.state.update(row, col, 2)
            return

        # Are they about to win?
        row, col = self.state.two_in_a_row(1)

        if row is not None and col is not None:
            self.state.update(row, col, 2)
            return

        # Is the center free?
        if self.state.empty(self.state.center_row(), self.state.center_col()):
            self.state.update(self.state.center_row(), self.state.center_col(), 2)
            return

        # Fall back to arbitrary
        row, col = self.state.first_free()
        self.state.update(row,col, 2)
