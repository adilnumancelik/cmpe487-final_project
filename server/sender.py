import socket
import threading
import _thread
import server.utils

def send_message_thread(receiver_ip_send, message):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
      server.settimeout(5.0)
      server.connect((receiver_ip_send, 12345))
      server.sendall(string_to_byte(message))

    except:
      remove(receiver_ip_send)
      server.close()