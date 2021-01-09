from enum import Enum


class GameState(Enum):
    WAITING = 1
    READY = 2
    QUESTION = 3
    MOVE = 4


class Game():

    def __init__(self, col, row):
        self.col = col
        self.row = row
        # Initially board is full of "Blank" places.
        self.board = [["B" for x in range(col)] for y in range(row)]
        self.state = GameState.WAITING
        self.players_names = [None, None]
        self.complete_lines = []
        self.turn = 1
        self.question = "Hey?"
        self.answer = "yEs."

