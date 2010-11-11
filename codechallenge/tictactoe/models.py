from django.db import models
from picklefield.fields import PickledObjectField

class GameState():
    '''Maintains game state in an internal data structure. This object is
    intended to be pickled for storage in the database. Access to the game
    state is done through (row,col) coordinates. For the purpose of this
    project, GameState creates an maintains a 3x3 board using a basic 2d array.
    '''

    def __init__(self):
        '''Construct a new GameState'''
        self.state = [[0,0,0],[0,0,0],[0,0,0]]

    def update(self, row, col, piece):
        '''Update the slot at row, col with the given piece. Piece can be
        anything as long as it's easily represented as a string.'''
        self.state[row][col] = piece

    def center_row(self):
        '''Return the row portion of the center slot coordinate'''
        # this would be more complicated in an NxN implementation. We can take
        # some liberties though since we're hardcoding 3x3.
        return 1

    def center_col(self):
        '''Return the col portion of the center slot coordinate'''
        # this would be more complicated in an NxN implementation. We can take
        # some liberties though since we're hardcoding 3x3.
        return 1

    def empty(self, row, col):
        '''Returns true if there is no piece at row, col; false otherwise.'''
        return not bool(self.state[row][col])

    def piece_at(self, row, col):
        '''Returns the piece at row,col'''
        return self.state[row][col]

    def first_free(self):
        '''Does a row major walk of the board to find the first empty slot. If
        the board is full, it returns (None, None)'''
        r,c = (0,0)
        for r in range(0,2):
            for c in range(0,2):
                if self.empty(r,c):
                    return (r,c)

        return (None, None)

    def could_win(self, piece):
        '''This method looks for a slot on the board that would result in a win
        for the player represented by the given piece. If no such slot exists,
        it returns (None, None)'''
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
    '''This model keeps track of a tictactoe game. It stores the game state and
    tracks when the game has been won (and by who).'''
    state  = PickledObjectField(default=GameState())
    name   = models.CharField(default="a tic tac toe game", max_length=50)
    over   = models.BooleanField()
    status = models.CharField(max_length=20, choices=(('tie', "It's a tie."), ('computer', 'Computer wins!')))

    def get_absolute_url(self):
        '''Used in the index and move views for redirecting.'''
        return r'/tictactoe/board/%i' % self.id

    def user_move(self, user_row, user_col):
        '''Handles a human user's move and reacts accordingly. This method
        implements an algorithm for never losing tic-tac-toe.'''
        if not self.state.empty(user_row,user_col):
            return

        self.state.update(user_row, user_col,'X')

        # Can I win?
        row, col = self.state.could_win('O')

        if row is not None and col is not None:
            self.state.update(row, col, 'O')
            self.over   = True
            self.status = 'computer'
            return

        # Are they about to win?
        row, col = self.state.could_win('X')

        if row is not None and col is not None:
            self.state.update(row, col, 'O')
            return

        # Is the center free?
        if self.state.empty(self.state.center_row(), self.state.center_col()):
            self.state.update(self.state.center_row(), self.state.center_col(), 'O')
            return

        # Fall back to arbitrary
        row, col = self.state.first_free()
        if row is not None and col is not None:
            self.state.update(row,col, 'O')
        else:
            self.over = True
            self.status = 'tie'
