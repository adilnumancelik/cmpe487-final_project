import socket
import threading
import _thread
import utils
import json
import sys
from game_controller import GameController 

PORT = 12345

def accept_connections():
  controller = GameController()
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('0.0.0.0', PORT)) 
    server.listen()
    print(f"Start to listen PORT: {PORT}")
    while True:
      try:
        conn, addr = server.accept()
        print(f"New connection request from {addr}")

        player_id = controller.add_connection(conn)
        threading.Thread(target=threaded_client, args=(conn, controller, player_id), daemon=True).start()
      except KeyboardInterrupt:
        print(f"Closing connections...")
        controller.close_connections()
        sys.exit()

      

def threaded_client(conn, controller, id):
  while True:
    data = conn.recv(1024)
    if not data:
      print(f"Player with {id} has been disconnected.")
      controller.remove_player(id)
      break
          
    message = json.loads(utils.byte_to_string(data))
    print(f"Receive message from Player {id}: {message}")

    if "TYPE" not in message or "PAYLOAD" not in message:
      print("Unkown type of message :(")
      continue

    if message["TYPE"] == "NAME":
      controller.enter_name(id, message["PAYLOAD"])
    elif message["TYPE"] == "MOVE":
      controller.move(id, message["PAYLOAD"])
    elif message["TYPE"] == "ANSWER":
      controller.give_turn(id)

accept_connections()