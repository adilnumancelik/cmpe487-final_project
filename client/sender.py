import socket
import threading
import _thread
import server.utils

def send_message(receiver_ip, port, message):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
      server.settimeout(5.0)
      server.connect((receiver_ip, port))
      server.sendall(server.utils.string_to_byte(message))

    except:
      server.close()