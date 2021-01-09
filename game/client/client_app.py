import utils
import time
import requests
import socket
import threading
import json
from game_controller import GameController
from tkinter import * 

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

# Initialize game.
control = GameController()

# Initialize GUI
board = Tk()
def move():
    pass
    #Label(board, text=f"{i}, {j}").pack()


q=Label(board, text=control.game.question, width="15", height="4").grid(row=0, column=0)
a=Entry(board, width="10")
a.grid(row=1, column=0)


def answer(event):
    text = "xd"
    ans = a.get()
    if ans == control.game.answer:
        text = "Correct answer."
    else:
        text = "Wrong answer."
    Label(board, text=text).grid(row = 3, column = 0)

b=Button(board, text = "Click here to answer.", command = answer, width = "15", height = "4").grid(row = 2, column=0)
a.bind('<Key-Return>',answer)

for i in range(control.game.col):
    for j in range(control.game.row):
        Button(board, text = control.game.board[i][j], command = move, width = "15", height = "4").grid(row = i, column=j+2)

board.mainloop()

'''
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

# Initialize GUI
root = Tk()  
# Code to add widget will go here…….. 
for i in range(control.game.col):
    for j in range(control.game.row):
        w = Label(root, text = control.game.board[i][j], width = "20", height = "5")  
        w.grid(row = i, column=j)  
root.mainloop()

# Join the listening thread.
y.join()
'''