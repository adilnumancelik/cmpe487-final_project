import threading
import pickle
import json
import sys
import random
import uuid
import time

sys.path.append('..')
from game import Game, GameState
from utils import string_to_byte, byte_to_string

class GameController():
    SPECIAL_KEYWORD = b"xaxaxayarmaW"
    MAX_RECEIVE_TIME_DIFFERENCE = 0.010 # in seconds

    def __init__(self):
        self.active_connections = [None, None] 
        self.game = Game(3, 3)
        self.lock = threading.Lock()
        self.receive_question_ts = [None, None]
        self.both_players_received = False
        self.calibration_acks = [[], []]
        self.calibrations = [[{} for _ in range(10)], [{} for _ in range(10)]]
        self.ts_difference = 0 # Average difference between timestamps of player 0 and 1.
        self.received_acks_cnt = [0, 0]
        self.ping_difference = 0

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
            self.calibration_acks = [[], []]
            self.calibrations = [[{} for _ in range(10)], [{} for _ in range(10)]]
            self.ts_difference = 0
            self.received_acks_cnt = [0, 0]
            self.ping_difference = 0


    def enter_name(self, id, name):
        ready = False

        def calibrate_timestamps(self):
            def connection_thread(self, conn, id, i):
                message = json.dumps({"TYPE": "CALIBRATION", "PAYLOAD": str(i)})
                self.calibrations[id][i]["server_send"] = time.time()
                conn.sendall(string_to_byte(message) + self.SPECIAL_KEYWORD)

            for i in range(10):
                for idx, conn in enumerate(self.active_connections):
                    if conn:
                        threading.Thread(target=connection_thread, args=(self, conn, idx, i), daemon=True).start()
                time.sleep(0.2)

        with self.lock:
            self.game.players_names[id] = name
            self.send_id(id)

            if self.game.players_names[1 - id] != None:
                ready = True

        if ready:
            threading.Thread(target=calibrate_timestamps, args=(self,), daemon=True).start()
            print("Hey")




    def notify_players(self):
        
        print("Sending Game information to the all players")

        def connection_thread(self, conn):
            conn.sendall(pickle.dumps(self.game) + self.SPECIAL_KEYWORD)

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
            self.game.question_uuid = str(uuid.uuid4())
            self.receive_question_ts = [None, None]
            self.both_players_received = False

        print("Generated the Question: " + question +  " / UUID: " + self.game.question_uuid)

    def send_id(self, id):
        conn = self.active_connections[id]

        message = {
            "TYPE": "ID",
            "PAYLOAD": id
        }

        print(f"Sending ID to the Player {id}")

        conn.sendall(string_to_byte(json.dumps(message)) + self.SPECIAL_KEYWORD)


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
                            for coordinate in sequence_coordinates:
                                self.game.marked_boxes.add(coordinate[0] * self.game.col + coordinate[1])

    def move(self, id, move):
        with self.lock:
            if self.game.state != GameState.MOVE or self.game.turn != id: # or not self.both_players_received:
                return

        coordinate_x, coordinate_y, character = move            
        
        self.calculate_score(id, coordinate_x, coordinate_y, character)
        self.generate_question()
        self.notify_players()
    
    def give_turn(self, id, question_uuid):
        with self.lock:
            print(self.game.state, self.game.question_uuid)
            if self.game.state != GameState.QUESTION or self.game.question_uuid != question_uuid:
                return 
            self.game.state = GameState.MOVE
            self.game.turn = id
        
        self.notify_players()
    
    # Returns the normalized timestamp difference between acknowledgment of two players in seconds. 
    def get_timestamp_diff(self):
        print("----> ", abs(self.receive_question_ts[0] - self.receive_question_ts[1] - self.ts_difference - self.ping_difference))
        return abs(self.receive_question_ts[0] - self.receive_question_ts[1] - self.ts_difference - self.ping_difference)

    def check_question_ack(self, id, timestamp, uuid):
        with self.lock:
            if self.game.question_uuid == uuid:
                self.receive_question_ts[id] = timestamp
                if self.receive_question_ts[1 - id]: 
                    if self.get_timestamp_diff() <= self.MAX_RECEIVE_TIME_DIFFERENCE:
                        print("Both player has received the question " + uuid)
                        self.both_players_received = True
                        return
                    else:
                        return
            else:
                return 

        time.sleep(0.2)

        with self.lock:
            if self.game.question_uuid != uuid:
                return

            if self.receive_question_ts[1 - id]: 
                if self.get_timestamp_diff() <= self.MAX_RECEIVE_TIME_DIFFERENCE:
                    self.both_players_received = True
                    print("Both player has received the question " + uuid)
                    return
                # else:
                #     self.update_time_difference()

        self.generate_question()
        self.notify_players()

    def add_calibration_ack(self, id, client_rec_ts, client_send_ts, ack_id):
        self.calibrations[id][ack_id]["server_rec"] = time.time()
        self.calibrations[id][ack_id]["client_rec"] = client_rec_ts
        self.calibrations[id][ack_id]["client_send"] = client_send_ts
        ready_to_start = False
        with self.lock:
            self.received_acks_cnt[id] += 1

            if self.received_acks_cnt[id] == 10 and self.received_acks_cnt[1 - id] == 10:
                ping0 = sum([(c["client_rec"]-c["server_send"]-c["client_send"]+c["server_rec"]) / 2 for c in self.calibrations[0][5:]]) / 5 
                ping1 = sum([(c["client_rec"]-c["server_send"]-c["client_send"]+c["server_rec"]) / 2 for c in self.calibrations[1][5:]]) / 5

                print("Player 0 has a ping: ", ping0 * 1000, " ms") 
                print("Player 1 has a ping: ", ping1 * 1000, " ms")

                self.ping_difference = ping0 - ping1
                self.game.wait_times = [max(0, -self.ping_difference), max(0, self.ping_difference)]

                delta0 = sum([(c["client_rec"]-c["server_send"]+c["client_send"]-c["server_rec"]) / 2 for c in self.calibrations[0][5:]]) / 5
                delta1 = sum([(c["client_rec"]-c["server_send"]+c["client_send"]-c["server_rec"]) / 2 for c in self.calibrations[1][5:]]) / 5
                self.ts_difference = delta0 - delta1
                print("Calculated time difference in seconds is: ", self.ts_difference)

                ready_to_start = True
        
        if ready_to_start:
            self.generate_question()
            self.notify_players()

     
