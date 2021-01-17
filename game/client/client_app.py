import utils
import time
import socket
import threading
import json
from game_controller import GameController
from tkinter import * 
from functools import partial
import sys
sys.path.append('..')

from game import Game, GameState

# Function that sends messages to the server.
def send_message(message_to_send):
    message_to_send=message_to_send+"xaxaxayarmaW"
    try:
        SERVER.sendall(utils.string_to_byte(message_to_send))
    except:
        print("Message could not be sent.")

# Function that listens to the server.
def listen_to_server():
    packets = []
    timestamp_r = 0
    timestamp_s = 0
    while True:
        data = None
        if len(packets) > 0:
            # print(packets[-1])
            data = packets[-1]
            packets.pop()
        else:
            try:
                # Receive message.
                from_server = SERVER.recv(1024).rstrip(b"xaxaxayarmaW")
                timestamp_r = time.time()
                control.time_received = timestamp_r
                # print(from_server)
                packets = from_server.split(b"xaxaxayarmaW")
                continue 
            except Exception as e: 
                print(e)
                return False   

        # Process message.
        question_id = control.process_message(data)
        
        timestamp_s=time.time()
        # If message is a question message, send the acknowledgement.
        if question_id != "-1" and not question_id.startswith("CAL"):
            ack_object= {"TYPE": "ACK", "QUESTION": question_id, "TIMESTAMP_R": timestamp_r, "TIMESTAMP_S": timestamp_s}
            ack=json.dumps(ack_object)
            send_message(ack)
        elif question_id.startswith("CAL"):
            timestamp_s=time.time()
            ack_object= {"TYPE": "CALIBRATION", "ID": question_id[3:], "TIMESTAMP_R": timestamp_r, "TIMESTAMP_S": timestamp_s}
            ack=json.dumps(ack_object)
            send_message(ack)  
        print(timestamp_r, timestamp_s)

# Construct connection.
PORT = 12345
SERVER_IP = "18.198.166.19"
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

def name_func(event):
    PLAYER_NAME = answer_form.get()
    PLAYER_NAME = PLAYER_NAME[:10]
    message_object= {"TYPE": "NAME","PAYLOAD": PLAYER_NAME}
    message=json.dumps(message_object)
    send_message(message)
    name_frame.destroy()

# Initialize GUI for player name.
name_frame = Tk()
name_frame.title("S0S")

mes = Label(name_frame, text="Enter your name (should be shorter than 10 characters): ", font=(None, 15)). grid(row = 0, column = 0, padx=5, pady=5)

answer_form=Entry(name_frame, width="30")
answer_form.grid(row=1, column=0, padx=5,pady=20,ipady=10)
answer_form.bind('<Key-Return>', name_func)

name_frame.mainloop()

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

# Function to handle answers.
def answer(event):
    timestamp_a=time.time()
    text = "xd"
    ans = answer_form.get()
    if control.game.state != GameState.QUESTION:
        if ans == control.game.answer:
            text = "Correct but your opponent was faster."
        else:
            text = "Wrong answer and opponent's was correct."
    elif ans == control.game.answer:
        text = "Correct answer."
        message_object= {"TYPE": "ANSWER","PAYLOAD": control.game.question_uuid, "DURATION": timestamp_a-control.time_received-cotnrol.game.wait_times[control.player_id]}
        message=json.dumps(message_object)
        send_message(message)
    else:
        text = "Wrong answer."
    feedback_message.set(text)

# Function to handle exit call.
def exit_func():
    board.destroy()
    # Closing the connection.
    SERVER.close()
    sys.exit()

# Function to handle restart call.
def restart_func():
    restart["state"] = "disabled"
    message_object= {"TYPE": "RESTART"}
    message=json.dumps(message_object)
    send_message(message)
    
# Set label for question.
question_var = StringVar()
question_var.set(control.game.question)
question=Label(board, textvariable=question_var, font=(None, 20), width="20", height="2").grid(row=0, column=0, padx=5, pady=5, columnspan=2)

# Set input for answer.
answer_form=Entry(board, width="30")
answer_form.grid(row=1, column=0, columnspan=2)
answer_form.bind('<Key-Return>', answer)

# Set label for feedback.
feedback_message = StringVar()
feedback_message.set("Type answer, press Enter.")
feedback = Label(board, textvariable=feedback_message, font=(None, 15)). grid(row = 0, column = 2, padx=5, pady=5, columnspan=5)

# Radio buttons for choosing S or O.
s = Radiobutton(board, text='S', font=(None, 20), variable=choice, value='S')
o = Radiobutton(board, text='O', font=(None, 20), variable=choice, value='O')
s.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
o.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

# Set score labels.
your_score=StringVar()
opponents_score=StringVar()
your_score.set(f"{control.game.players_names[control.player_id]}'s score: {control.game.scores[control.player_id]}")
opponents_score.set(f"{control.game.players_names[1-control.player_id]}'s score: {control.game.scores[1-control.player_id]}") 
your = Label(board, textvariable=your_score, font=(None, 20)).grid(row = 4, column = 0, padx=5, pady=5, columnspan=2)
opponent = Label(board, textvariable=opponents_score, font=(None, 20)).grid(row = 5, column = 0, padx=5, pady=5, columnspan=2)

# Set exit button.
ex = Button(board, text="EXIT", font=(None, 20), command=exit_func).grid(row = 6, column = 0, padx=5, pady=5)
# Set restart button.
restart=Button(board, text="RESTART", font=(None, 20), command=restart_func)
restart.grid(row=6, column=1, padx=5, pady=5)
restart["state"] = "disabled"

# Set board button variables.
button_vars=[]
for i in range(control.game.col):
    for j in range(control.game.row):
        button_vars.append(StringVar())
        button_vars[i*control.game.col+j].set(control.game.board[i][j])

# Create board buttons list.
buttons=[]
for i in range(control.game.col):
    for j in range(control.game.row):
        # Create buttons.
        action_with_arg = partial(move, i, j)
        buttons.append(Button(board, textvariable = button_vars[i*control.game.col+j], font=(None, 20), command = action_with_arg, width = "7", height = "3"))
        buttons[i*control.game.col+j].grid(row = i+1, column=j+3, padx=5, pady=5)
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

        your_score.set(f"{control.game.players_names[control.player_id]}'s score: {control.game.scores[control.player_id]}")
        opponents_score.set(f"{control.game.players_names[1-control.player_id]}'s score: {control.game.scores[1-control.player_id]}")             
        
        # Delete content of answer form.
        answer_form.delete(0,END)
        
        # Update board button and text color variables.
        
        for i in range(control.game.col):
            for j in range(control.game.row):
                coor = i*control.game.col+j 
                button_vars[i*control.game.col+j].set(control.game.board[i][j])
                if control.game.state != GameState.MOVE or control.game.turn != control.player_id or control.game.board[i][j] != "":
                    buttons[i*control.game.col+j]["state"] = "disabled"
                else:
                    buttons[i*control.game.col+j]["state"] = "normal"
                if coor in control.game.marked_boxes:
                    buttons[i*control.game.col+j].configure(disabledforeground = "red")
                else:
                    buttons[i*control.game.col+j].configure(disabledforeground = "black")
        if control.isFinished():
            if control.game.scores[control.player_id] > control.game.scores[1-control.player_id]:
                feedback_message.set("Game over. You won.")
            elif control.game.scores[control.player_id] < control.game.scores[1-control.player_id]:
                feedback_message.set(f"Game over. You lost.")
            else:
                feedback_message.set(f"Game over. Tied.")

            restart["state"] = "normal"
        else:
            restart["state"] = "disabled" 

        control.UPDATE_FLAG = False

    board.after(10, update)
update()
board.mainloop()

# Closing the connection.
SERVER.close()

# Exit the program.
sys.exit()