import sender
import utils
import time
import requests
import socket
import threading
'''
f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)
print(MY_IP)
'''
MY_IP = "188.3.160.244"
MY_PORT = 12345

SERVER_IP = "52.203.72.10"
PORT = 12345
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.settimeout(5.0)
SERVER.connect((SERVER_IP, PORT))

message = "keko değilsin"
sender.send_message(SERVER, SERVER_IP, PORT, message)
threading.Thread(target=sender.listen_to_server, args=(SERVER, ), daemon=True).start()
time.sleep(5)
sender.send_message(SERVER, SERVER_IP, PORT, "5 sn geçti")
time.sleep(5)
sender.send_message(SERVER, SERVER_IP, PORT, "10 sn geçti")
time.sleep(1000)