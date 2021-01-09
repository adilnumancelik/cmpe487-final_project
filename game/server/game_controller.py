import threading
import pickle

import sys
sys.path.append('..')

from game import Game, GameState

class GameController():

    def __init__(self):
        self.active_connections = [None, None] 
        self.game = Game(10, 10)
        self.lock = threading.Lock()

    def add_connection(self, conn):
        id = 1
        if self.active_connections[0] == None:
            id = 0
        
        self.active_connections[id] = conn
        return id


    def remove_player(id):
        with self.lock:
            self.active_connections[id] = None
            self.game.players_names[id] = None
            self.game.state = GameState.WAITING
        notify_players()


    def enter_name(self, id, name):
        with self.lock:
            self.game.players_names[id] = name
            send_id(id)
            if self.game.players_names[1 - id] != None:
                self.game.state = GameState.READY
                notify_players()


    def notify_players(self):
        message = {
            "TYPE": "GAME",
            "PAYLOAD": pickle.dumps(self.game)
        }
        for conn in self.active_connections:
            conn.sendall(json.dumps(message))

    def send_id(self, id):
        conn = self.active_connections[id]

        message = {
            "TYPE": "ID",
            "PAYLOAD": id
        }

        conn.sendall(json.dumps(message))


    def move(self, id, index):
        pass 
    
    def check_answer(self, id, index):
        pass