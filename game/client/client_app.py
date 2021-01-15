import utils
import time
import requests
import socket
import threading
import json
from game_controller import GameController
from tkinter import * 
from functools import partial
import sys
sys.path.append('..')

from game import Game, GameState

def send_message(message_to_send):
    try:
        SERVER.sendall(utils.string_to_byte(message_to_send))
    except:
        print("Message could not be sent.")

def listen_to_server():
    while True:
        try:
            # Receive message.
            from_server = SERVER.recv(4096)
            # Process message.
            question_id = control.process_message(from_server)
            
            timestamp = time.time()
            # If message is a question message, send the acknowledgement.
            if question_id != "-1":
                ack_object= {"TYPE": "ACK", "QUESTION": question_id, "TIMESTAMP": timestamp}
                ack=json.dumps(ack_object)
                send_message(ack)
            elif question_id != "CAL"
                ack_object= {"TYPE": "CALIBRATION", "TIMESTAMP": timestamp}
                ack=json.dumps(ack_object)
                send_message(ack)
        except Exception as e: 
            print(e)
            return False   
'''
# Initialize game.
control = GameController()
for i in range(control.game.col):
    for j in range(control.game.row):
        control.game.board[i][j]=i*control.game.col+j

# Initialize GUI
board = Tk()
board.title("S0S")

#Function to handle moves. 
def move(i,j):

    print(f"{i}, {j}")
    #Label(board, text=f"{i}, {j}").pack()

# Function to handle answers.
def answer(event):
    text = "xd"
    ans = answer_form.get()
    if ans == control.game.answer:
        text = "Correct answer."
        message_object= {"TYPE": "ANSWER","PAYLOAD": control.game.question_uuid}
        message=json.dumps(message_object)
        send_message(message)
    else:
        text = "Wrong answer."
    feedback_message.set(text)

# Set label for feedback.
feedback_message = StringVar()
feedback_message.set("Type answer, press Enter.")
feedback = Label(board, textvariable=feedback_message).grid(row = 2, column = 0)

question=Label(board, text=control.game.question, width="25", height="4").grid(row=0, column=0)

# Input form answer.
answer_form=Entry(board, width="10")
answer_form.grid(row=1, column=0)
answer_form.bind('<Key-Return>', answer)

# b=Button(board, text = "Click here to answer.", command = answer, width = "15", height = "4").grid(row = 2, column=0)

# Create board buttons.
buttons=[]
for i in range(control.game.col):
    for j in range(control.game.row):
        action_with_arg = partial(move, i, j)
        buttons.append(Button(board, text = control.game.board[i][j], command = action_with_arg, width = "15", height = "4"))
        buttons[i*control.game.col+j].grid(row = i, column=j+2)

board.mainloop()
'''


# Find my ip.
f = requests.request('GET', 'http://myip.dnsomatic.com')
MY_IP = str(f.text)

# Construct connection.
PORT = 12345
SERVER_IP = "18.198.166.19"
# SERVER_IP = "3.230.114.17"
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
board = Tk()
board.title("S0S")

# Variable that holds if user selected S or O.
choice = StringVar()
choice.set('S')

#Function to handle moves. 
def move(i,j):
    message_object = "xd"
    SorO = choice.get()
    if SorO == 'S':
        message_object= {"TYPE": "MOVE","PAYLOAD": [i, j, "S"]}
    else:
        message_object= {"TYPE": "MOVE","PAYLOAD": [i, j, "O"]}
    message=json.dumps(message_object)
    send_message(message)
    # print(f"{i}, {j}")
    #Label(board, text=f"{i}, {j}").pack()

# Function to handle answers.
def answer(event):
    text = "xd"
    ans = answer_form.get()
    if ans == control.game.answer:
        text = "Correct answer."
        message_object= {"TYPE": "ANSWER","PAYLOAD": control.game.question_uuid}
        message=json.dumps(message_object)
        send_message(message)
    else:
        text = "Wrong answer."
    feedback_message.set(text)

# Set label for question.
question_var = StringVar()
question_var.set(control.game.question)
question=Label(board, textvariable=question_var, font=(None, 20), width="8", height="2").grid(row=0, column=0, padx=5, pady=5)

# Set input for answer.
answer_form=Entry(board, width="10")
answer_form.grid(row=1, column=0)
answer_form.bind('<Key-Return>', answer)

# Set label for feedback.
feedback_message = StringVar()
feedback_message.set("Type answer, press Enter.")
feedback = Label(board, textvariable=feedback_message, font=(None, 20)). grid(row = 2, column = 0, padx=5, pady=5)


s = Radiobutton(board, text='S', font=(None, 20), variable=choice, value='S')
o = Radiobutton(board, text='O', font=(None, 20), variable=choice, value='O')
s.grid(row=3, column=0, padx=5, pady=5)
o.grid(row=4, column=0, padx=5, pady=5)

'''
# Set button for picking S or O.
a=Button(board, text="Pick S", command = S, width="25", height="4")
a.grid(row=3, column=0)
b=Button(board, text="Pick O", command = O, width="25", height="4")
b.grid(row=4, column=0)
'''
# Set score labels.
your_score=StringVar()
opponents_score=StringVar()
your_score.set(f"Your score: {control.game.scores[control.player_id]}")
opponents_score.set(f"Opponent's score: {control.game.scores[1-control.player_id]}") 
your = Label(board, textvariable=your_score, font=(None, 20)).grid(row = 5, column = 0, padx=5, pady=5)
opponent = Label(board, textvariable=opponents_score, font=(None, 20)).grid(row = 6, column = 0, padx=5, pady=5)


# Set board button variables.
button_vars=[]
for i in range(control.game.col):
    for j in range(control.game.row):
        button_vars.append(StringVar())
        button_vars[i*control.game.col+j].set(control.game.board[i][j])

# Create board buttons.
buttons=[]
for i in range(control.game.col):
    for j in range(control.game.row):
        action_with_arg = partial(move, i, j)
        buttons.append(Button(board, textvariable = button_vars[i*control.game.col+j], font=(None, 20), command = action_with_arg, width = "5", height = "2"))
        buttons[i*control.game.col+j].grid(row = i, column=j+2, padx=5, pady=5)
        buttons[i*control.game.col+j]["state"] = "disabled"

def update():
    if control.UPDATE_FLAG == True:  
        # Set feedback message and question variables.
        if control.game.state == GameState.QUESTION:
            feedback_message.set("Type answer, press Enter.")
            question_var.set(control.game.question)
        elif control.game.state == GameState.MOVE:
            question_var.set("") 
            if control.game.turn == control.player_id:
                feedback_message.set("Make your move.")
            else:
                feedback_message.set("Wait, it is not your turn.")
        elif control.game.state == GameState.WAITING:
            question_var.set("")
            feedback_message.set("Wait your opponent to connect.")

        your_score.set(f"Your score: {control.game.scores[control.player_id]}")
        opponents_score.set(f"Opponent's score: {control.game.scores[1-control.player_id]}")             
        
        # Input form answer.
        # answer_form['text']=""
        
        # Update board button variables.
        for i in range(control.game.col):
            for j in range(control.game.row):
                button_vars[i*control.game.col+j].set(control.game.board[i][j])
                if control.game.state != GameState.MOVE or control.game.turn != control.player_id:
                    buttons[i*control.game.col+j]["state"] = "disabled"
                else:
                    buttons[i*control.game.col+j]["state"] = "normal"

        control.UPDATE_FLAG = False

    board.after(10, update)
update()
board.mainloop()

# Join the listening thread.
y.join()

# Closing the connection.
SERVER.close()