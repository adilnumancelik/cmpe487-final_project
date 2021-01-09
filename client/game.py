from enum import Enum

class Game():
    state = GameState.WAITING
    players_names = [None, None]
    board = [][]
    col = 0
    row = 0
    complete_lines = []
    turn = 1
    question = "Hey?"
    answer = "yEs."

    def __init__(self, col, row):
        self.col = col
        self.row = row
        # Initially board is full of "Blank" places.
        board = [["B" for x in range(col)] for y in range(row)]

    
    
class GameState(Enum):
    WAITING = 1
    QUESTION = 2
    MOVE = 3