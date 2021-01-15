import pickle
import sys
import json

sys.path.append('..')

from game import Game, GameState

class GameController():

    def __init__(self):
        self.game = Game(7, 7)
        self.player_id = 0
        self.UPDATE_FLAG = False

    def process_message(self, inc_message):
        
        try:
            inc_message_o=json.loads(inc_message)
            if inc_message_o["TYPE"] == "ID":
                self.player_id = int(inc_message_o["PAYLOAD"])
                return "-1"
        except:
            self.game = pickle.loads(inc_message)
            self.UPDATE_FLAG = True
            if self.game.state == GameState.QUESTION:
                return self.game.question_uuid
            else:
                return "-1"
