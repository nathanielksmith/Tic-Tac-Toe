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

    def piece_at(self, row, col):
        return self.state[row][col]

    def first_free(self):
        r,c = (0,0)
        for r in range(0,2):
            for c in range(0,2):
                if self.empty(r,c):
                    return (r,c)

        return (None, None)
    
    def could_win(self, piece):
        # inspired by http://stackoverflow.com/questions/1056316/algorithm-for-determining-tic-tac-toe-game-over-java/1056352#1056352
        for r in range(0,3):
            for c in range(0,3):
                if self.piece_at(r,c) != piece:
                    continue

                # check diag
                if r == c:
                    has_piece = [(i,i) for i in range(0,3) if self.piece_at(i,i) == piece]
                    is_empty  = [(i,i) for i in range(0,3) if self.empty(i,i)]
                    if len(has_piece) == 2 and len(is_empty) == 1:
                        return is_empty.pop()

                # check antidiag
                if (r,c) in [(0,2),(2,0),(1,1)]:
                    has_piece = [(i,2-i) for i in range(0,3) if self.piece_at(i,2-i) == piece]
                    is_empty  = [(i,2-i) for i in range(0,3) if self.empty(i,2-i)]
                    if len(has_piece) == 2 and len(is_empty) == 1:
                        return is_empty.pop()

                # check row
                has_piece = [(i,c) for i in range(0,3) if self.piece_at(i,c) == piece]
                is_empty  = [(i,c) for i in range(0,3) if self.empty(i,c)]
                if len(has_piece) == 2 and len(is_empty) == 1:
                    return is_empty.pop()
                    
                # check col
                has_piece = [(r,i) for i in range(0,3) if self.piece_at(r,i) == piece]
                is_empty  = [(r,i) for i in range(0,3) if self.empty(r,i)]
                if len(has_piece) == 2 and len(is_empty) == 1:
                    return is_empty.pop()

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
        row, col = self.state.could_win(2)

        if row is not None and col is not None:
            self.state.update(row, col, 2)
            self.over   = True
            self.status = 'computer' 
            return

        # Are they about to win?
        row, col = self.state.could_win(1)

        if row is not None and col is not None:
            self.state.update(row, col, 2)
            return

        # Is the center free?
        if self.state.empty(self.state.center_row(), self.state.center_col()):
            self.state.update(self.state.center_row(), self.state.center_col(), 2)
            return

        # Fall back to arbitrary
        row, col = self.state.first_free()
        if row is not None and col is not None:
            self.state.update(row,col, 2)
        else:
            self.over = True
            self.status = 'tie'


