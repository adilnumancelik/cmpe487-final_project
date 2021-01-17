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
        self.board = [["" for x in range(col)] for y in range(row)]
        self.state = GameState.WAITING
        self.players_names = [None, None]
        self.complete_lines = []
        self.turn = 1
        self.question = "Wait your opponent."
        self.question_uuid = ""
        self.answer = "yEs."
        self.scores = [0, 0]
        self.marked_boxes = set([])
        self.wait_times = [0, 0]

    def reset_board(self):
        self.board = [["" for x in range(self.col)] for y in range(self.row)]
        self.scores = [0, 0]
        self.marked_boxes = set([])
        self.complete_lines = []

