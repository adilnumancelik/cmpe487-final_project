import threading
import sys
sys.path.append('..')

from game import Game, GameState

class GameController():

    def __init__(self):
        self.active_connections = [] 
        self.game = Game(10, 10)
        self.lock = threading.Lock()

    def add_connection(self, conn):
        self.active_connections.append(conn)
    
    def enter_name(self, id, name):
        with self.lock:
            self.game.players_names[id] = name

            if self.game.players_names[1 - id] != None:
                self.game.state = GameState.READY

    def move(self, id, index):
        pass 
    
    def check_answer(self, id, index):
        pass