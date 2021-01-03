import socket
import threading
import _thread
import utils
# import game_control

def send_message(server, receiver_ip, port, message):
    try:
        server.sendall(utils.string_to_byte(message))
    except:
        print("Message could not be sent.")

def listen_to_server(server):
    while True:
        try:
            from_server = server.recv(4096)
            # threading.Thread(target=utils.process_message, args=(from_server, ), daemon=True).start()
            #game_control.process_message(from_server)
            print(from_server)
        except: 
            print("Server timed out.")
            return False   