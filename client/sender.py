import socket
import threading
import _thread
import utils

def send_message(receiver_ip, port, message):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
      server.settimeout(5.0)
      server.connect((receiver_ip, port))
      server.sendall(utils.string_to_byte(message))
      from_server = server.recv(4096)
      print(utils.byte_to_string(from_server))

    except:
      print("no")
      server.close()