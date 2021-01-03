import network
import utils
import time
import requests
import socket
import threading
from game import Game
import json
'''
f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)
print(MY_IP)
'''


MY_IP = "188.3.160.244"
MY_PORT = 12345
SERVER_IP = "52.203.72.10"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.settimeout(5.0)
SERVER.connect((SERVER_IP, MY_PORT))
PLAYER_NAME = "keko1"
game = Game()

message_object= {"TYPE": "NAME","PAYLOAD": PLAYER_NAME}
message=json.dumps(message_object)
threading.Thread(target=network.listen_to_server, args=(SERVER, ), daemon=True).start()
network.send_message(SERVER, SERVER_IP, PORT, message)

