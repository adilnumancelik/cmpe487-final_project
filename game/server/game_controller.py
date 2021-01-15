import threading
import pickle
import json
import sys
import random
import uuid

sys.path.append('..')
from game import Game, GameState
from utils import string_to_byte, byte_to_string

class GameController():

    MAX_RECEIVE_TIME_DIFFERENCE = 0.050 # in seconds

    def __init__(self):
        self.active_connections = [None, None] 
        self.game = Game(7, 7)
        self.lock = threading.Lock()
        self.receive_question_ts = [None, None]
        self.both_players_received = False


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
            self.game.reset_board()



    def enter_name(self, id, name):
        with self.lock:
            self.game.players_names[id] = name
            self.send_id(id)

        if self.game.players_names[1 - id] != None:
            self.generate_question()
            self.notify_players()


    def notify_players(self):
        
        print("Sending Game information to the all players")

        def connection_thread(self, conn):
            conn.sendall(pickle.dumps(self.game))

        for conn in self.active_connections:
            if conn:
                threading.Thread(target=connection_thread, args=(self, conn), daemon=True).start()


    def generate_question(self):
        print("Generating New Question...")
        operator_list = ["+", "-", "*"]
        operator = random.choice(operator_list)

        limit = 20 if operator == "*" else 100

        number_1 = random.randint(1, limit)
        number_2 = random.randint(1, limit)

        question = str(number_1) + operator + str(number_2)
        answer = str(eval(question))

        with self.lock:
            self.game.state = GameState.QUESTION
            self.game.question = question
            self.game.answer = answer
            self.question_uuid = str(uuid.uuid4())
            self.receive_question_ts = [None, None]
            self.both_players_received = False

        print("Generated the Question: " + question)

    def send_id(self, id):
        conn = self.active_connections[id]

        message = {
            "TYPE": "ID",
            "PAYLOAD": id
        }

        print(f"Sending ID to the Player {id}")

        conn.sendall(string_to_byte(json.dumps(message)))


    def close_connections(self):
        for conn in self.active_connections:
            if conn:
                conn.close()


    def calculate_score(self, id, coordinate_x, coordinate_y, character):
        directions = [[-1, 0], [-1, -1], [0, -1], [1, -1]]

        with self.lock:
            self.game.board[coordinate_x][coordinate_y] = character

            for x in range(coordinate_x - 1, coordinate_x + 2):
                for y in range(coordinate_y - 1, coordinate_y + 2):
                    for direction in directions:
                        sequence = ""
                        sequence_coordinates = []
                        for i in range(3):
                            sequence_coordinates.append([x - (i - 1) * direction[0], y - (i - 1) * direction[1]])
                            
                            if sequence_coordinates[-1][0] < 0 or sequence_coordinates[-1][1] < 0 or \
                                sequence_coordinates[-1][0] >= self.game.row or sequence_coordinates[-1][1] >= self.game.col:
                                sequence = "NOO"
                                break

                            sequence += self.game.board[sequence_coordinates[-1][0]][sequence_coordinates[-1][1]]

                        if sequence == "SOS" and sequence_coordinates not in self.game.complete_lines:
                            self.game.scores[id] += 1
                            self.game.complete_lines.append(sequence_coordinates)

    def move(self, id, move):
        with self.lock:
            if self.game.state != GameState.MOVE or self.game.turn != id or not self.both_players_received:
                return

        coordinate_x, coordinate_y, character = move            
        
        self.calculate_score(id, coordinate_x, coordinate_y, character)
        self.generate_question()
        self.notify_players()
    
    def give_turn(self, id, question_uuid):
        with self.lock:
            if self.game.state != GameState.QUESTION or self.game.question_uuid != question_uuid:
                return 
            self.game.state = GameState.MOVE
            self.game.turn = id
        
        self.notify_players()

    def check_question_ack(self, id, timestamp, uuid):
        with self.lock:
            if self.game.question_uuid == uuid:
                self.receive_question_ts[id] = timestamp
                if self.receive_question_ts[1 - id]  and abs(self.receive_question_ts[1 - id] - timestamp) <= MAX_RECEIVE_TIME_DIFFERENCE:
                    self.both_players_received = True
                    return
            else:
                return 

        sleep(MAX_RECEIVE_TIME_DIFFERENCE)

        with self.lock:
            if self.receive_question_ts[1 - id] and abs(self.receive_question_ts[1 - id] - timestamp) <= MAX_RECEIVE_TIME_DIFFERENCE:
                self.both_players_received = True
                return

        self.generate_question()
        self.notify_players()
     
