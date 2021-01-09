import pickle
import sys
import json

sys.path.append('..')

from game import Game, GameState

class GameController():

    def __init__(self):
        self.game = Game(10, 10)
        self.player_id = -1

    def process_message(self, inc_message):
        
        try:
            inc_message_o=json.loads(inc_message)
            if inc_message_o["TYPE"] == "ID":
                self.player_id = int(inc_message_o["PAYLOAD"])
        except:
            self.game = pickle.loads(inc_message)
