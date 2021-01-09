import threading
import pickle
import json
import sys
sys.path.append('..')

from game import Game, GameState
from utils import string_to_byte, byte_to_string

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


    def remove_player(self, id):
        with self.lock:
            self.active_connections[id] = None
            self.game.players_names[id] = None
            self.game.state = GameState.WAITING
        self.notify_players()


    def enter_name(self, id, name):
        with self.lock:
            self.game.players_names[id] = name
            self.send_id(id)
            if self.game.players_names[1 - id] != None:
                self.game.state = GameState.READY
                self.notify_players()


    def notify_players(self):
        for conn in self.active_connections:
            if conn:
                conn.sendall(pickle.dumps(self.game))


    def send_id(self, id):
        conn = self.active_connections[id]

        message = {
            "TYPE": "ID",
            "PAYLOAD": id
        }

        conn.sendall(string_to_byte(json.dumps(message)))


    def close_connections(self):
        for conn in self.active_connections:
            if conn:
                conn.close()

    def move(self, id, index):
        pass 
    
    def check_answer(self, id, index):
        pass