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
        self.game = Game(4, 4)
        self.lock = threading.Lock()
        self.receive_question_ts = [None, None]
        self.both_players_received = False
        self.calibration_acks = [[], []]
        self.calibrations = [[{} for _ in range(10)], [{} for _ in range(10)]]
        self.ts_difference = 0 # Average difference between timestamps of player 0 and 1.
        self.received_acks_cnt = [0, 0]
        self.ping_difference = 0
        self.ts_info = [{}, {}]
        self.answer_ts = [None, None]

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
        self.notify_players()

    def restart_game(self):
        with self.lock:
            self.game.reset_board()

        self.generate_question()
        self.notify_players()


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



    def notify_players(self):
        
        print("Sending Game information to the all players")

        def connection_thread(self, conn, id):
            if self.game.state == GameState.QUESTION:
                self.ts_info[id][self.game.question_uuid] = {}
                self.ts_info[id][self.game.question_uuid]["server_send"] = time.time()
            conn.sendall(pickle.dumps(self.game) + self.SPECIAL_KEYWORD)

        for idx, conn in enumerate(self.active_connections):
            if conn:
                threading.Thread(target=connection_thread, args=(self, conn, idx), daemon=True).start()


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
            self.answer_ts = [None, None]

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
    
    def give_turn(self, id, question_uuid, duration):
        with self.lock:
            if self.game.state != GameState.QUESTION or self.game.question_uuid != question_uuid:
                return 
            
            self.answer_ts[id] = duration
            if self.answer_ts[1 - id]:
                return
        
        if not self.answer_ts[1 - id]:
            time.sleep(abs(2 * self.ping_difference))
        
        with self.lock:
            self.game.state = GameState.MOVE

            if self.answer_ts[1-id] and self.answer_ts[1-id] < self.answer_ts[id]:
                self.game.turn = 1 - id
            else:
                self.game.turn = id
        
        self.notify_players()
    
    # Returns the normalized timestamp difference between acknowledgment of two players in seconds. 
    def get_timestamp_diff(self):
        return abs(self.receive_question_ts[0] - self.receive_question_ts[1] - self.ts_difference - self.ping_difference)

    def check_question_ack(self, id, client_rec, client_send, uuid):
        

        self.ts_info[id][uuid]["server_rec"] = time.time()
        self.ts_info[id][uuid]["client_rec"] = client_rec
        self.ts_info[id][uuid]["client_send"] = client_send

        with self.lock:
            if self.game.state != GameState.QUESTION:
                return
            if self.game.question_uuid == uuid:
                self.receive_question_ts[id] = client_rec
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
                    self.add_new_calibration_ts(uuid)
                    return
                else:
                    self.add_new_calibration_ts(uuid)

        self.generate_question()
        self.notify_players()

    def add_new_calibration_ts(self, uuid):
        self.calibrations[0].append(self.ts_info[0][uuid])
        self.calibrations[0] = self.calibrations[0][1:]

        self.calibrations[1].append(self.ts_info[1][uuid])
        self.calibrations[1] = self.calibrations[1][1:]
        self.update_time_difference()


    def update_time_difference(self):        
        ping0 = sum([(c["client_rec"]-c["server_send"]-c["client_send"]+c["server_rec"]) / 2 for c in self.calibrations[0][-6:]]) / 6 
        ping1 = sum([(c["client_rec"]-c["server_send"]-c["client_send"]+c["server_rec"]) / 2 for c in self.calibrations[1][-6:]]) / 6

        print("Player 0 has a ping: ", ping0 * 1000, " ms") 
        print("Player 1 has a ping: ", ping1 * 1000, " ms")

        self.ping_difference = ping0 - ping1
        self.game.wait_times = [max(0, -self.ping_difference), max(0, self.ping_difference)]

        delta0 = sum([(c["client_rec"]-c["server_send"]+c["client_send"]-c["server_rec"]) / 2 for c in self.calibrations[0][-6:]]) / 6
        delta1 = sum([(c["client_rec"]-c["server_send"]+c["client_send"]-c["server_rec"]) / 2 for c in self.calibrations[1][-6:]]) / 6
        self.ts_difference = delta0 - delta1
        print("Calculated time difference in seconds is: ", self.ts_difference)
        

    def add_calibration_ack(self, id, client_rec_ts, client_send_ts, ack_id):
        self.calibrations[id][ack_id]["server_rec"] = time.time()
        self.calibrations[id][ack_id]["client_rec"] = client_rec_ts
        self.calibrations[id][ack_id]["client_send"] = client_send_ts
        ready_to_start = False
        with self.lock:
            self.received_acks_cnt[id] += 1

            if self.received_acks_cnt[id] == 10 and self.received_acks_cnt[1 - id] == 10:
                self.update_time_difference()
                ready_to_start = True
        
        if ready_to_start:
            self.generate_question()
            self.notify_players()

     
