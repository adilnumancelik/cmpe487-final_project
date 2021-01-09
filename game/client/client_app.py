import utils
import time
import requests
import socket
import threading
import json
from game import Game
from game_controller import GameController

f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)
# MY_IP = "188.3.160.244"
print(MY_IP)
PORT = 12345
SERVER_IP = "52.203.72.10"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.settimeout(25.0)

global is_message_received = False
global control = GameController()

def initialize():
    global is_message_received
    global control
    # Connect to the server.
    try:
        SERVER.connect((SERVER_IP, MY_PORT))
    except:
        print("Server does not respond.")
        exit()
    
    # Send player name to server.
    PLAYER_NAME = "keko1"
    message_object= {"TYPE": "NAME","PAYLOAD": PLAYER_NAME}
    message=json.dumps(message_object)
    send_message(SERVER, SERVER_IP, MY_PORT, message)
    
    # Start listening to the server.
    y=threading.Thread(target=listen_to_server, args=(SERVER, ), daemon=True)
    y.start()

    while True:
        while not is_message_received:
            pass
        control.process_message()


    y.join()

def send_message(message):
    try:
        server.sendall(utils.string_to_byte(message))
    except:
        print("Message could not be sent.")

def listen_to_server():
    global is_message_received
    global control
    while True:
        try:
            from_server = SERVER.recv(4096)
            # Send the timestamp immediately.
            timestamp = time.time()
            message_object= {"TYPE": "ACK","PAYLOAD": timestamp}
            send_message(message)
            # threading.Thread(target=control.process_message, args=(from_server, ), daemon=True).start()
            # Process the incoming message.
            is_message_received = True
            control.received_message = utils.byte_to_string(from_server)
        except: 
            print("Server timed out.")
            return False   


initialize()