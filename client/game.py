class Game():
    state = "waiting"
    players_names = ["fhs2lkh21sda.6fs231", "fhs2lkh21sda.6fs231"]
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

    
    
