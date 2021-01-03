import network
import utils
import time
import requests
import socket
import threading
import json
from game import Game
'''
f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)
print(MY_IP)
'''

game = Game(10,10)
MY_IP = "188.3.160.244"
print(MY_IP)
MY_PORT = 12345
SERVER_IP = "52.203.72.10"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.settimeout(25.0)
try:
    SERVER.connect((SERVER_IP, MY_PORT))
except:
    print("Server does not respond.")
    exit()
PLAYER_NAME = "keko1"
print(PLAYER_NAME)

message_object= {"TYPE": "NAME","PAYLOAD": PLAYER_NAME}
message=json.dumps(message_object)

network.send_message(SERVER, SERVER_IP, MY_PORT, message)
y=threading.Thread(target=network.listen_to_server, args=(SERVER, ), daemon=True)
y.start()
print(message)
y.join()
