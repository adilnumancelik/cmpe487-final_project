import socket
import threading
import _thread
import utils

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
            utils.process_message(from_server)
        except: 
            pass   