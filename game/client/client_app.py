import utils
import time
import requests
import socket
import threading
import json
from game_controller import GameController
# import Tkinter
# import tkMessageBox



def send_message(message_to_send):
    try:
        SERVER.sendall(utils.string_to_byte(message_to_send))
    except:
        print("Message could not be sent.")

def listen_to_server():
    while True:
        try:
            from_server = SERVER.recv(4096)
            print(from_server)
            # Send the timestamp immediately.
            timestamp = time.time()
            ack_object= {"TYPE": "ACK","PAYLOAD": timestamp}
            ack=json.dumps(ack_object)
            send_message(ack)

            # Process the incoming message.
            control.process_message(from_server)
        except Exception as e: 
            print(e)
            return False   

# Find my ip.
f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)

# Construct connection.
PORT = 12345
SERVER_IP = "3.230.114.17"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server.
try:
    SERVER.connect((SERVER_IP, PORT))
except:
    print("Server does not respond.")
    exit()

# Initialize game.
control = GameController()

# Start listening to the server.
y=threading.Thread(target=listen_to_server, daemon=True)
y.start()

# Send player name to server.
PLAYER_NAME = input("Enter your name: ")
message_object= {"TYPE": "NAME","PAYLOAD": PLAYER_NAME}
message=json.dumps(message_object)
send_message(message)




''''
# Initialize GUI
top = Tkinter.Tk()

def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()
'''
i = 0

while i<4:
    time.sleep(5)
    print(control.game.board)
    print(control.player_id)
    i+=1

y.join()
